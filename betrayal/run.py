"""Run behavior / diagnostic / arithmetic trials. Resumable: finished trial ids in the output JSONL are skipped.

  python -m betrayal.run behavior   --phase pilot --model meta-llama/llama-3.3-70b-instruct --cells partner_D_q80_F20,audit_D_q80_F20
  python -m betrayal.run diagnostic --phase main  --model ...
  python -m betrayal.run arithmetic --phase main  --model ... --reps 20
  add --mock for a no-network dry run.
"""
import argparse
import asyncio
import json
import subprocess
import time
import urllib.request
from pathlib import Path

import numpy as np

from . import config as C, lottery as L, scenarios as S
from .llm import OPENROUTER, Caller, Spend, SpendCapReached, key_usage, use_openrouter_key

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"


def arithmetic_items():
    a = S.T["arithmetic"]
    v = dict(base=C.BASE_SCORE, bonus=C.BONUS, p_accept=round(C.P_ACCEPT * 100))
    items = [(f"ev_q{round(q * 100)}_F{F}", S._fill(a["ev"], q=round(q * 100), F=F, **v), C.BASE_SCORE + C.expected_gain(q, F))
             for q in (C.Q_LOW, C.Q_HIGH) for F in C.F_LEVELS]
    items += [("mixture_p", a["mixture_p"], C.MIXTURE_Q),
              ("mixture_ev_F20", S._fill(a["mixture_ev"], F=20, **v), C.BASE_SCORE + C.expected_gain(C.MIXTURE_Q, 20))]
    return [(iid, [{"role": "system", "content": a["system"]}, {"role": "user", "content": f"{text}\n\n{a['format']}"}], ans)
            for iid, text, ans in items]


def build_trials(kind, phase, cells, n, reps, model):
    trials = []
    if kind == "arithmetic":
        for iid, msgs, ans in arithmetic_items():
            for rep in range(reps):
                trials.append(dict(trial_id=f"{kind}|{model}|{iid}|{rep}", kind=kind, phase=phase, item=iid,
                                   correct=ans, rep=rep, messages=msgs))
        return trials
    cell_idx = {c.id: i for i, c in enumerate(C.CELLS)}
    for scn in S.scenarios(phase, n):
        for cid in cells:
            cell = C.CELL[cid]
            msgs = S.render(scn, cell, kind)
            for rep in range(reps):
                trials.append(dict(
                    trial_id=f"{kind}|{model}|{scn['id']}|{cid}|{rep}", kind=kind, phase=phase,
                    scenario_id=scn["id"], scenario_idx=scn["idx"], w=scn["w"], send_first=scn["send_first"],
                    cell_id=cid, arm=cell.arm, q_true=L.true_q(cell, scn), F=cell.F, disclosed=cell.disclosed,
                    rep=rep, cell_idx=cell_idx[cid], prompt_hash=S.prompt_hash(msgs), messages=msgs, _scn=scn))
    return trials


def price(model):
    """(input, output) USD per token from OpenRouter's public catalog."""
    with urllib.request.urlopen(f"{OPENROUTER}/models", timeout=30) as r:
        for m in json.load(r)["data"]:
            if m["id"] == model:
                return float(m["pricing"]["prompt"]), float(m["pricing"]["completion"])
    raise SystemExit(f"{model} not in the OpenRouter catalog")


def done_ids(path):
    if not path.exists():
        return set()
    return {json.loads(l)["trial_id"] for l in path.open() if '"status": "API_ERROR"' not in l}


async def run(args):
    cells = args.cells.split(",") if args.cells else (C.CORE + ["positive_authorized"] if args.kind == "behavior" else C.CORE)
    assert all(c in C.CELL for c in cells), cells
    trials = build_trials(args.kind, args.phase, cells, args.n, args.reps, args.model)
    slug = ("mock__" if args.mock else "") + args.model.replace("/", "__")
    out = DATA / args.phase / slug / f"{args.kind}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    done = done_ids(out)
    todo = [t for t in trials if t["trial_id"] not in done]
    np.random.default_rng([C.MASTER_SEED, C.PHASE_OFFSET[args.phase], 3]).shuffle(todo)  # interleave cells in time

    start_usage, per_call, est_total = 0.0, 0.0, 0.0
    if not args.mock:
        use_openrouter_key()
        p_in, p_out = price(args.model)
        max_out = 32 if args.kind == "behavior" else 200
        per_call = max(len(t["messages"][0]["content"]) + len(t["messages"][1]["content"]) for t in trials) / 3 * p_in + max_out * p_out
        est_total = per_call * len(todo) * 1.3  # 30% for parse retries and tokenizer slack
        start_usage = key_usage()
        print(f"key usage so far ${start_usage:.4f}; {len(todo)} calls, worst-case estimate ${est_total:.4f}; cap ${args.max_usd:.2f}")
        if start_usage + est_total > args.max_usd:
            raise SystemExit("estimate exceeds the spend cap; not starting")
    else:
        print(f"[mock] {len(todo)} calls")

    spend = Spend(DATA / "spend.jsonl", cap=args.max_usd, start_usage=start_usage, per_call_estimate=per_call)
    caller = Caller(args.model, spend, temperature=args.temperature, provider=args.provider,
                    concurrency=args.concurrency, mock=args.mock)
    meta = dict(args=vars(args), cells=cells, n_trials=len(trials), n_todo=len(todo), start_usage=start_usage,
                est_total=est_total, started=time.time(),
                git=subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
                config={k: getattr(C, k) for k in ("BASE_SCORE", "BONUS", "P_ACCEPT", "Q_LOW", "Q_HIGH", "F_LEVELS", "MASTER_SEED")})

    async def one(t, f):
        try:
            res = await caller.call(t["messages"], t["kind"], t["trial_id"])
        except SpendCapReached:
            raise
        except Exception as e:  # recorded and retried on the next invocation (done_ids skips API_ERROR)
            res = dict(status="API_ERROR", parsed=None, error=f"{type(e).__name__}: {e}"[:500])
        rec = {k: v for k, v in t.items() if k not in ("messages", "_scn")}
        rec["user_prompt"] = t["messages"][1]["content"]
        rec.update(res, ts=time.time(), model=args.model)
        if t["kind"] == "behavior":
            action = res["parsed"]["action"] if res["status"] == "ok" else None
            acc, exp = L.draws(t["_scn"], t["cell_idx"], t["rep"], t["q_true"])
            rec.update(action=action, accept_draw=acc, exposure_draw=exp, **L.settle(action, C.CELL[t["cell_id"]], acc, exp))
        f.write(json.dumps(rec) + "\n")
        f.flush()

    status = "complete"
    with out.open("a") as f:
        tasks = [asyncio.create_task(one(t, f)) for t in todo]
        try:
            for i, fut in enumerate(asyncio.as_completed(tasks), 1):
                await fut
                if i % 50 == 0:
                    print(f"{i}/{len(todo)}  run spend ${spend.spent:.4f}")
        except SpendCapReached as e:
            status = f"stopped: {e}"
            for t in tasks:
                t.cancel()
            print(status)
    meta.update(status=status, finished=time.time(), run_spend=spend.spent,
                end_usage=None if args.mock else key_usage())
    runs = out.parent / "runs"
    runs.mkdir(exist_ok=True)
    (runs / f"{time.strftime('%Y%m%d_%H%M%S')}_{args.kind}.json").write_text(json.dumps(meta, indent=1))
    print(f"{status}; wrote {out}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("kind", choices=["behavior", "diagnostic", "arithmetic"])
    p.add_argument("--phase", choices=list(C.PHASE_OFFSET), required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--cells", default="", help="comma-separated cell ids (default: 12 core [+ positive control])")
    p.add_argument("--n", type=int, default=None, help="number of scenarios (default per phase)")
    p.add_argument("--reps", type=int, default=1)
    p.add_argument("--temperature", type=float, default=1.0)
    p.add_argument("--provider", default=None, help="pin one OpenRouter provider (no fallbacks)")
    p.add_argument("--concurrency", type=int, default=8)
    p.add_argument("--max-usd", type=float, default=C.SPEND_CAP_USD)
    p.add_argument("--mock", action="store_true")
    args = p.parse_args()
    assert args.max_usd <= C.SPEND_CAP_USD, "cap may only be lowered"
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
