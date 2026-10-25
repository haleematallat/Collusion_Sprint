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


def arithmetic_items(fmt="format"):
    a = S.T["arithmetic"]
    v = dict(base=C.BASE_SCORE, bonus=C.BONUS, p_accept=round(C.P_ACCEPT * 100))
    items = [(f"ev_q{round(q * 100)}_F{F}", S._fill(a["ev"], q=round(q * 100), F=F, **v), C.BASE_SCORE + C.expected_gain(q, F))
             for q in (C.Q_LOW, C.Q_HIGH) for F in C.F_LEVELS]
    items += [("mixture_p", a["mixture_p"], C.MIXTURE_Q),
              ("mixture_ev_F20", S._fill(a["mixture_ev"], F=20, **v), C.BASE_SCORE + C.expected_gain(C.MIXTURE_Q, 20))]
    return [(iid, [{"role": "system", "content": a["system"]}, {"role": "user", "content": f"{text}\n\n{a[fmt]}"}], ans)
            for iid, text, ans in items]


def build_trials(kind, phase, cells, n, reps, model):
    trials = []
    if kind.startswith("arithmetic"):
        for iid, msgs, ans in arithmetic_items("format" + kind[10:]):
            for rep in range(reps):
                trials.append(dict(trial_id=f"{kind}|{model}|{iid}|{rep}", kind=kind, phase=phase, item=iid,
                                   correct=ans, rep=rep, messages=msgs))
        return trials
    if phase in S2_PHASES:
        return build_s2_trials(kind, phase, cells, n, reps, model)
    if phase in C.S3_PHASES:
        return build_s3_trials(phase, cells, n, reps, model)
    if phase in C.S3B_PHASES:
        return build_s3b_trials(phase, cells, n, reps, model)
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


S2_PHASES = ("pilot2", "main2")
S2_DIAG_CELLS = ["S10", "R1", "R1_summary", "S80", "R8", "R8_summary"]


def s2_cell(cid, model):
    """'R1@F60' -> (S2Cell, 60); without '@F' the penalty comes from the pilot-chosen C.S2_F[model]."""
    base, _, f = cid.partition("@F")
    cell = C.S2_CELL[base]
    return cell, int(f) if f else C.S2_F[model][cell.risk]


def build_s2_trials(kind, phase, cells, n, reps, model):
    trials = []
    for scn in S.scenarios(phase, n):
        for cid in cells:
            cell, F = s2_cell(cid, model)
            msgs = S.render_s2(scn, cell, F, kind)
            q = C.S2_Q[cell.risk]
            # Study-1 Cell for the shared lottery/settlement code: authorized offers are never penalized
            settle_cell = C.Cell(f"{cell.id}@F{F}", "positive" if cell.auth else "partner", q, F, True)
            for rep in range(reps):
                trials.append(dict(
                    trial_id=f"{kind}|{model}|{scn['id']}|{cell.id}@F{F}|{rep}", kind=kind, phase=phase,
                    scenario_id=scn["id"], scenario_idx=scn["idx"], w=scn["w"], send_first=scn["send_first"],
                    cell_id=cell.id, F=F, risk=cell.risk, fmt=cell.fmt, extra=cell.extra, auth=cell.auth,
                    pos=cell.pos, order=cell.order, reported_episodes=sorted(S.report_positions(scn, cell)) if cell.fmt == "record" else [],
                    arm=settle_cell.arm, q_true=q, rep=rep, cell_idx=100 + C.S2_CELLS.index(cell),
                    prompt_hash=S.prompt_hash(msgs), messages=msgs, _scn=scn, _cell=settle_cell))
    return trials


def build_s3_trials(phase, cells, n, reps, model):
    trials = []
    for scn in S.scenarios(phase, n):
        for cid in cells:
            base, _, fs = cid.partition("@FS")   # 'M3_E@FS11': pilot re-check of the override penalty
            cell = C.S3_CELL[base]
            F_s = int(fs) if fs else C.s3_fs(model, cell)
            msgs, ids = S.render_s3(scn, cell, model, F_s)
            for rep in range(reps):
                trials.append(dict(
                    trial_id=f"behavior|{model}|{scn['id']}|{cid}|{rep}", kind="behavior3" + ("_m2" if cell.menu == "M2" else ""),
                    phase=phase, scenario_id=scn["id"], scenario_idx=scn["idx"], w=scn["w"], perm=scn["perm"], order=ids,
                    cell_id=cid, risk=cell.risk, pos=cell.pos, menu=cell.menu, d=cell.d, dom=cell.dom,
                    score_instr=cell.score_instr, q_true=C.S2_Q[cell.risk], F=C.S3_F[model], F_s=F_s,
                    rep=rep, prompt_hash=S.prompt_hash(msgs), messages=msgs, _scn=scn))
    return trials


def build_s3b_trials(phase, cells, n, reps, model):
    hist = {h["scenario_id"]: h for h in map(json.loads, (DATA / phase / "history.jsonl").open())}
    trials = []
    for scn in S.scenarios(phase, n):
        for cid in cells:
            base, _, f = cid.partition("@F")   # 'E@F40': pilot F selection
            cell = C.S3B_CELL[base]
            F = int(f) if f else C.S3B_F[model]
            msgs = S.render_s3b(scn, cell, F, hist[scn["id"]])
            for rep in range(reps):
                trials.append(dict(
                    trial_id=f"behavior|{model}|{scn['id']}|{cid}|{rep}", kind="behavior3b" + ("" if cell.draft else "_act"),
                    phase=phase, scenario_id=scn["id"], scenario_idx=scn["idx"], send_first=scn["send_first"], cell_id=cid,
                    pos=cell.pos, draft_first=cell.draft, auth=cell.auth, F=F, k=hist[scn["id"]]["k"], rep=rep,
                    prompt_hash=S.prompt_hash(msgs), messages=msgs, _scn=scn))
    return trials


def price(model):
    """(input, output) USD per token from OpenRouter's public catalog."""
    with urllib.request.urlopen(f"{OPENROUTER}/models", timeout=30) as r:
        for m in json.load(r)["data"]:
            if m["id"] == model:
                return float(m["pricing"]["prompt"]), float(m["pricing"]["completion"])
    raise SystemExit(f"{model} not in the OpenRouter catalog")


def observed_cost(slug, kind):
    """Mean measured cost per call for this model and kind from earlier runs, or None."""
    costs = [r["usage"][-1]["cost"] for p in DATA.glob(f"*/{slug}/{kind}.jsonl") for r in map(json.loads, p.open())
             if r.get("usage")]
    return float(np.mean(costs)) if costs else None


def done_ids(path):
    if not path.exists():
        return set()
    return {json.loads(l)["trial_id"] for l in path.open() if '"status": "API_ERROR"' not in l}


async def run(args):
    if args.phase in C.S3B_PHASES:
        cells = args.cells.split(",") if args.cells else ["E", "L"]
        assert args.kind == "behavior" and all(c.partition("@F")[0] in C.S3B_CELL for c in cells), cells
    elif args.phase in C.S3_PHASES:
        cells = args.cells.split(",") if args.cells else C.S3_MAIN
        assert args.kind == "behavior" and all(c.partition("@FS")[0] in C.S3_CELL for c in cells), cells
    elif args.phase in S2_PHASES:
        cells = args.cells.split(",") if args.cells else (
            [c.id for c in C.S2_CELLS] if args.kind == "behavior" else S2_DIAG_CELLS)
        assert all(s2_cell(c, args.model) for c in cells), cells
    else:
        cells = args.cells.split(",") if args.cells else (C.CORE + ["authorized_offer_positive_control"] if args.kind == "behavior" else C.CORE + ["neutral_U_F20"])
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
        per_call = max(len(t["messages"][0]["content"]) + len(t["messages"][1]["content"]) for t in trials) / 3 * p_in + C.MAX_TOKENS * p_out
        # projection uses measured cost when available; the per-call guard (Spend.check) stays worst-case
        measured = observed_cost(slug, args.kind)
        est_total = (measured or per_call) * len(todo) * 1.3  # 30% for parse retries and tokenizer slack
        start_usage = key_usage()
        print(f"key usage so far ${start_usage:.4f}; {len(todo)} calls, estimate ${est_total:.4f} "
              f"({'measured' if measured else 'worst-case'} per-call cost); cap ${args.max_usd:.2f}")
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
        rec = {k: v for k, v in t.items() if k not in ("messages", "_scn", "_cell")}
        rec["user_prompt"] = t["messages"][1]["content"]
        rec.update(res, ts=time.time(), model=args.model)
        if t["kind"].startswith("behavior3b"):   # B settles sent drafts later (betrayal.verifier score), with this u
            ok = res["status"] == "ok"
            rec.update(action=res["parsed"]["action"] if ok else None, draft=res["parsed"].get("draft") if ok else None,
                       u=L.draws_s3(t["_scn"], t["rep"]))
        elif t["kind"].startswith("behavior3"):
            action = res["parsed"]["action"] if res["status"] == "ok" else None
            u = L.draws_s3(t["_scn"], t["rep"])
            rec.update(action=action, u=u, **L.settle_s3(action, t["q_true"], t["d"], t["F"], t["F_s"], u))
        elif t["kind"] == "behavior":
            action = res["parsed"]["action"] if res["status"] == "ok" else None
            acc, exp = L.draws(t["_scn"], t["cell_idx"], t["rep"], t["q_true"])
            rec.update(action=action, accept_draw=acc, exposure_draw=exp, **L.settle(action, t.get("_cell") or C.CELL[t["cell_id"]], acc, exp))
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
    p.add_argument("kind", choices=["behavior", "diagnostic", "diagnostic_work", "arithmetic", "arithmetic_work"])
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
