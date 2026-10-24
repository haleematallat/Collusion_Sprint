"""Spend guard halts before the cap; parsing, refusal and parse-failure coding."""
import asyncio
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from betrayal import llm


class FakeCompletions:
    def __init__(self, texts, cost):
        self.texts, self.cost, self.calls = list(texts), cost, 0

    async def create(self, **kw):
        self.calls += 1
        t = self.texts[min(self.calls - 1, len(self.texts) - 1)]
        return SimpleNamespace(usage=SimpleNamespace(model_dump=lambda: {"cost": self.cost, "prompt_tokens": 900}),
                               choices=[SimpleNamespace(message=SimpleNamespace(content=t, refusal=None), finish_reason="stop")],
                               model="fake/model", provider="FakeProv")


def caller(tmp_path, texts, cost=0.5, start=7.0, monkeypatch=None):
    monkeypatch.setenv("OPENROUTER_API_KEY", "dummy-not-a-key")
    spend = llm.Spend(Path(tmp_path) / "spend.jsonl", cap=8.0, start_usage=start, per_call_estimate=0.01)
    c = llm.Caller("meta-llama/llama-3.3-70b-instruct", spend)
    fake = FakeCompletions(texts, cost)
    c.client = SimpleNamespace(chat=SimpleNamespace(completions=fake))
    return c, fake


MSG = [{"role": "system", "content": "s"}, {"role": "user", "content": "u"}]


def test_spend_cap_stops_before_next_call(tmp_path, monkeypatch):
    c, fake = caller(tmp_path, ['{"action": "NO_OFFER"}'], monkeypatch=monkeypatch)

    async def go():
        for i in range(5):
            await c.call(MSG, "behavior", f"t{i}")

    with pytest.raises(llm.SpendCapReached):
        asyncio.run(go())
    assert fake.calls == 2  # 7.0 + 0.5 + 0.5 = 8.0; a third call would exceed $8
    assert len((tmp_path / "spend.jsonl").read_text().splitlines()) == 2


def test_status_coding(tmp_path, monkeypatch):
    run = lambda texts, kind="behavior": asyncio.run(caller(tmp_path, texts, cost=0.0, start=0.0, monkeypatch=monkeypatch)[0].call(MSG, kind, "t"))
    ok = run(['{"action": "SEND_OFFER"}'])
    assert ok["status"] == "ok" and ok["parsed"] == {"action": "SEND_OFFER"} and ok["attempts"] == 1
    assert run(["I cannot help with arranging that."])["status"] == "REFUSAL"
    pf = run(["maybe", "SEND", '{"action": "YES"}'])
    assert pf["status"] == "PARSE_FAIL" and pf["attempts"] == 3
    assert run(["oops", '{"action": "NO_OFFER"}'])["attempts"] == 2
    d = run(['{"p_exposure": 0.45, "penalty_points": 20, "expected_score_send": 50.6, "expected_score_no_send": 50}'], "diagnostic")
    assert d["status"] == "ok"


def test_parse_strictness():
    assert llm.parse("behavior", 'Sure: {"action": "NO_OFFER"}') == {"action": "NO_OFFER"}
    assert llm.parse("behavior", '{"action": "send_offer"}') is None
    assert llm.parse("arithmetic", '{"answer": true}') is None
    assert llm.parse("arithmetic", '{"answer": 50.6}') == {"answer": 50.6}
