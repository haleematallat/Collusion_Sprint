"""One OpenRouter call with strict JSON output, parse retries, refusal coding and a hard spend guard."""
import asyncio
import json
import os
import re
import time
import urllib.request
from pathlib import Path

from . import config as C

OPENROUTER = "https://openrouter.ai/api/v1"


def _schema(name, props, required):
    return {"type": "json_schema", "json_schema": {"name": name, "strict": True, "schema": {
        "type": "object", "properties": props, "required": required, "additionalProperties": False}}}


SCHEMAS = {
    "behavior": _schema("decision", {"action": {"type": "string", "enum": list(C.ACTIONS)}}, ["action"]),
    "diagnostic": _schema("diagnostic", {k: {"type": "number"} for k in C.DIAG_FIELDS}, list(C.DIAG_FIELDS)),
    "arithmetic": _schema("answer", {"answer": {"type": "number"}}, ["answer"]),
}
REFUSAL_RE = re.compile(r"\b(I can(?:not|'t)|I won'?t|I will not|I'?m unable|I am unable|I must decline|"
                        r"not (?:able|comfortable) to|cannot (?:assist|help|comply|participate))", re.I)


def parse(kind, text):
    """Return the validated JSON dict, or None."""
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    if kind == "behavior":
        return d if d.get("action") in C.ACTIONS else None
    keys = C.DIAG_FIELDS if kind == "diagnostic" else ("answer",)
    ok = all(isinstance(d.get(k), (int, float)) and not isinstance(d.get(k), bool) for k in keys)
    return {k: d[k] for k in keys} if ok else None


def key_usage():
    """Total USD already spent on the key, read from OpenRouter (free endpoint)."""
    req = urllib.request.Request(f"{OPENROUTER}/key", headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return float(json.load(r)["data"]["usage"])


def use_openrouter_key():
    # the user's key lives in `open_router_key`; poseidon_compute reads OPENROUTER_API_KEY. Never written to disk.
    if not os.environ.get("OPENROUTER_API_KEY") and os.environ.get("open_router_key"):
        os.environ["OPENROUTER_API_KEY"] = os.environ["open_router_key"]
    if not os.environ.get("OPENROUTER_API_KEY"):
        raise SystemExit("No OpenRouter key: set open_router_key or OPENROUTER_API_KEY.")


class SpendCapReached(RuntimeError):
    pass


class Spend:
    """Stops before a call would push total key usage past the cap. Ledger: one JSON line per paid call."""

    def __init__(self, ledger: Path, cap=C.SPEND_CAP_USD, start_usage=0.0, per_call_estimate=0.0):
        self.ledger, self.cap, self.start, self.est, self.spent = ledger, cap, start_usage, per_call_estimate, 0.0

    def check(self):
        if self.start + self.spent + self.est > self.cap:
            raise SpendCapReached(f"spend cap ${self.cap:.2f}: key usage {self.start:.4f} + this run {self.spent:.4f}")

    def add(self, cost, model, trial_id):
        self.spent += cost
        # a call whose cost the API did not report still raises the running total via the estimate
        self.est = max(self.est, cost)
        self.ledger.parent.mkdir(parents=True, exist_ok=True)
        with self.ledger.open("a") as f:
            f.write(json.dumps({"ts": time.time(), "model": model, "trial_id": trial_id, "cost": cost}) + "\n")


class Caller:
    def __init__(self, model, spend: Spend, temperature=1.0, provider=None, concurrency=8, mock=False):
        self.model, self.spend, self.temperature, self.provider, self.mock = model, spend, temperature, provider, mock
        self.sem = asyncio.Semaphore(concurrency)
        self.use_schema = True
        if not mock:
            from poseidon_compute import make_client, resolve_model
            if resolve_model(model) != model:
                raise SystemExit(f"poseidon_compute would rewrite {model!r} -> {resolve_model(model)!r}; refusing.")
            self.client = make_client(async_=True, timeout=120, max_retries=0)

    async def _once(self, messages, kind, max_tokens, trial_id):
        if self.mock:
            return _mock_reply(messages, kind), {"cost": 0.0}, "mock", self.model
        self.spend.check()
        extra = {"usage": {"include": True}}
        if self.provider:
            extra["provider"] = {"order": [self.provider], "allow_fallbacks": False, "require_parameters": True}
        kw = dict(model=self.model, messages=messages, temperature=self.temperature, max_tokens=max_tokens, extra_body=extra)
        if self.use_schema:
            kw["response_format"] = SCHEMAS[kind]
        r = await self.client.chat.completions.create(**kw)
        u = r.usage.model_dump() if r.usage else {}
        cost = float(u.get("cost") or 0.0) or self.spend.est  # shortcut: estimate if unreported, upgrade if it happens often
        self.spend.add(cost, self.model, trial_id)
        msg = r.choices[0].message
        text = msg.content or ""
        if getattr(msg, "refusal", None):
            text = "REFUSAL::" + msg.refusal
        return text, dict(u, cost=cost, finish=r.choices[0].finish_reason), getattr(r, "provider", None), r.model

    async def call(self, messages, kind, trial_id, max_tokens=None, parse_attempts=3):
        """Returns dict(status, parsed, raw, attempts, usage, provider, model_returned, schema_mode)."""
        max_tokens = max_tokens or C.MAX_TOKENS
        msgs, raws, usage = list(messages), [], []
        async with self.sem:
            for attempt in range(1, parse_attempts + 1):
                text, u, prov, mret = await self._with_backoff(msgs, kind, max_tokens, trial_id)
                raws.append(text)
                usage.append(u)
                parsed = None if text.startswith("REFUSAL::") else parse(kind, text)
                if parsed is not None:
                    status = "ok"
                    break
                if text.startswith("REFUSAL::") or REFUSAL_RE.search(text):
                    status = "REFUSAL"
                    break
                status = "PARSE_FAIL"
                msgs = msgs + [{"role": "assistant", "content": text},
                               {"role": "user", "content": "Your reply was not valid. Respond with JSON only, exactly in the requested format."}]
        return dict(status=status, parsed=parsed, raw=raws, attempts=attempt, usage=usage, provider=prov,
                    model_returned=mret, schema_mode="json_schema" if self.use_schema else "prompt_only")

    async def _with_backoff(self, msgs, kind, max_tokens, trial_id, tries=6):
        from openai import APIStatusError, APIConnectionError, APITimeoutError, RateLimitError
        for i in range(tries):
            try:
                return await self._once(msgs, kind, max_tokens, trial_id)
            except SpendCapReached:
                raise
            except APIStatusError as e:
                # provider without json_schema support: fall back to the JSON format already stated in the prompt
                msg = str(e).lower()
                if self.use_schema and e.status_code in (400, 404) and any(
                        k in msg for k in ("response_format", "json_schema", "structured", "no endpoints")):
                    self.use_schema = False
                    continue
                if not (isinstance(e, RateLimitError) or e.status_code >= 500) or i == tries - 1:
                    raise
            except (APIConnectionError, APITimeoutError):
                if i == tries - 1:
                    raise
            await asyncio.sleep(2 ** i)


def _mock_reply(messages, kind):
    """Deterministic fake model for dry runs: no network, no spend."""
    import hashlib
    h = int(hashlib.sha256(messages[-1]["content"].encode()).hexdigest(), 16)
    if kind == "behavior":
        return json.dumps({"action": C.ACTIONS[h % 2]})
    if kind == "diagnostic":
        return json.dumps({"p_exposure": 0.45, "penalty_points": 20, "expected_score_send": 50.6, "expected_score_no_send": 50})
    return json.dumps({"answer": 50.6})
