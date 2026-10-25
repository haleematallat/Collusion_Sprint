"""Validity checks A-E re-run on the recorded confirmatory data (for the report appendix).

  python -m betrayal.validate --phase main --model deepseek/deepseek-v3.2
"""
import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from . import config as C, lottery as L, scenarios as S
from .analyze import ROOT, load


def check(df):
    out = {}
    # A. lottery: draws exist for every trial, so rates use all trials, not only SEND trials
    acc = df["accept_draw"].astype(bool)
    out["A_accept_rate"] = dict(rate=acc.mean(), n=len(df), target=C.P_ACCEPT,
                                p=stats.binomtest(int(acc.sum()), len(df), C.P_ACCEPT).pvalue)
    for q in (C.Q_LOW, C.Q_HIGH):
        g = df[(df["q_true"] == q) & (df["arm"] != "positive")]
        e = g["exposure_draw"].astype(bool)
        out[f"A_exposure_rate_q{round(q * 100)}"] = dict(rate=e.mean(), n=len(g), target=q,
                                                         p=stats.binomtest(int(e.sum()), len(g), q).pvalue)
        a, b = g["accept_draw"].astype(bool), e
        t = np.array([[(a & b).sum(), (a & ~b).sum()], [(~a & b).sum(), (~a & ~b).sum()]])
        out[f"A_independence_q{round(q * 100)}_chi2_p"] = stats.chi2_contingency(t)[1]
    # A/E. settlement recomputed from the logged draws and action
    bad = 0
    for r in df.itertuples():
        s = L.settle(r.action, C.CELL[r.cell_id], r.accept_draw, r.exposure_draw)
        bad += any(not (getattr(r, k) == v or (pd.isna(getattr(r, k)) and v is None)) for k, v in s.items())
    out["E_settlement_mismatches"] = bad
    out["E_no_offer_score_changes"] = int(((df["action"] != "SEND_OFFER") & (df["score"] != C.BASE_SCORE)).sum())
    sent = df[df["sent"]]
    out["E_realized"] = dict(sent=len(sent), accepted=int(sent["accepted"].sum()), exposed=int(sent["exposed"].sum()),
                             exposed_by=dict(Counter(sent["exposed_by"].dropna())), mean_score_sent=sent["score"].mean(),
                             mean_score_not_sent=df[~df["sent"]]["score"].mean())
    # B. leakage: logged prompts of the two hidden types are identical per scenario
    u = df[df["cell_id"].str.startswith("partner_U") & (df["rep"] == 0)]
    pairs = u.assign(F=u["cell_id"].str[-3:]).groupby(["scenario_id", "F"])["user_prompt"].nunique()
    out["B_undisclosed_prompt_pairs"] = dict(n=len(pairs), identical=int((pairs == 1).sum()))
    # B. logged prompts equal the code's rendering (nothing extra was sent)
    scns = {s["id"]: s for s in S.scenarios(df["phase"].iloc[0])}
    out["B_logged_prompt_mismatches"] = int(sum(S.render(scns[r.scenario_id], C.CELL[r.cell_id])[1]["content"] != r.user_prompt
                                                for r in df.itertuples()))
    # D. matching: partner vs audit prompts differ only in "- " exposure lines
    m = df[df["cell_id"].isin(C.PRIMARY) & (df["rep"] == 0)].pivot(index="scenario_id", columns="cell_id", values="user_prompt")
    diff_other = sum(any(not l.startswith("- ") for l in set(p.splitlines()) ^ set(a.splitlines()))
                     for p, a in zip(m[C.PRIMARY[0]], m[C.PRIMARY[1]]))
    out["D_primary_pairs"] = dict(n=len(m), differ_outside_exposure_lines=int(diff_other))
    # C. positive control and status
    pc = df[df["cell_id"] == "authorized_offer_positive_control"]["y"]
    out["C_positive_control_send_rate"] = dict(rate=pc.mean(), n=int(pc.notna().sum()))
    out["status_counts"] = dict(Counter(df["status"]))
    out["providers"] = dict(Counter(df["provider"]))
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--phase", default="main")
    p.add_argument("--model", required=True)
    a = p.parse_args()
    slug = a.model.replace("/", "__")
    df = load(ROOT / "data" / a.phase / slug / "behavior.jsonl")
    res = check_s3(df) if a.phase in C.S3_PHASES else check_s2(df) if a.phase in ("pilot2", "main2") else check(df)
    out = ROOT / "results" / a.phase / slug
    out.mkdir(parents=True, exist_ok=True)
    (out / "validation.json").write_text(json.dumps(res, indent=1, default=float))
    print(json.dumps(res, indent=1, default=float))



def check_s2(df):
    """Study 2 checks on recorded trials: lotteries, settlement, logged prompts, record contents, providers."""
    out = {}
    acc = df["accept_draw"].astype(bool)
    out["A_accept_rate"] = dict(rate=acc.mean(), n=len(df), p=stats.binomtest(int(acc.sum()), len(df), C.P_ACCEPT).pvalue)
    for q in (C.Q_LOW, C.Q_HIGH):
        g = df[(df["q_true"] == q) & ~df["auth"]]
        e = g["exposure_draw"].astype(bool)
        out[f"A_exposure_rate_q{round(q * 100)}"] = dict(rate=e.mean(), n=len(g), p=stats.binomtest(int(e.sum()), len(g), q).pvalue)
    bad = 0
    for r in df.itertuples():
        cell = C.Cell(f"{r.cell_id}@F{r.F}", r.arm, r.q_true, r.F, True)
        s = L.settle(r.action, cell, r.accept_draw, r.exposure_draw)
        bad += any(not (getattr(r, k) == v or (pd.isna(getattr(r, k)) and v is None)) for k, v in s.items())
    out["E_settlement_mismatches"] = bad
    out["E_auth_penalties"] = int(df[df["auth"]]["penalty"].sum())
    out["E_no_offer_score_changes"] = int(((df["action"] != "SEND_OFFER") & (df["score"] != C.BASE_SCORE)).sum())
    scns = {s["id"]: s for s in S.scenarios(df["phase"].iloc[0])}
    out["B_logged_prompt_mismatches"] = int(sum(
        S.render_s2(scns[r.scenario_id], C.S2_CELL[r.cell_id], r.F)[1]["content"] != r.user_prompt for r in df.itertuples()))
    rec = df[df["fmt"] == "record"]
    out["B_record_report_counts_ok"] = bool(all(len(x) == C.S2_REPORTS[k] for x, k in zip(rec["reported_episodes"], rec["risk"])))
    # the same scenario shows the identical record in R, R+summary, R+placebo (and R8 = AUTH_R8)
    shared = rec[rec["pos"] == "random"].assign(key=lambda d: d["risk"]).groupby(["scenario_id", "key"])["reported_episodes"] \
        .apply(lambda s: len({tuple(x) for x in s}))
    out["B_records_shared_within_scenario"] = bool((shared == 1).all())
    out["status_counts"] = dict(Counter(df["status"]))
    out["providers"] = dict(Counter(df["provider"]))
    out["F_by_risk"] = {k: sorted(set(v)) for k, v in df.groupby("risk")["F"]}
    return out



def check_s3(df):
    """Study 3a checks: lottery rates, common random numbers, settlement, logged prompts, statuses, providers."""
    out = {}
    u = np.array(df.drop_duplicates(["scenario_id", "rep"])["u"].tolist())   # one lottery per (scenario, rep)
    for j, (name, p) in enumerate((("accept", C.P_ACCEPT), ("report_q10", C.Q_LOW), ("detect", C.S3_D))):
        k = int((u[:, j] < p).sum())
        out[f"A_{name}_rate"] = dict(rate=k / len(u), n=len(u), p=stats.binomtest(k, len(u), p).pvalue)
    out["A_common_random_numbers"] = bool((df.groupby(["scenario_id", "rep"])["u"].apply(lambda s: len({tuple(x) for x in s})) == 1).all())
    bad = sum(any(getattr(r, k) != v for k, v in L.settle_s3(r.action, r.q_true, r.d, r.F, r.F_s, r.u).items()) for r in df.itertuples())
    out["E_settlement_mismatches"] = bad
    model = df["model"].iloc[0]
    scns = {s["id"]: s for s in S.scenarios(df["phase"].iloc[0])}
    out["B_logged_prompt_mismatches"] = int(sum(S.render_s3(scns[r.scenario_id], C.S3_CELL[r.cell_id], model)[0][1]["content"] != r.user_prompt
                                                for r in df.itertuples()))
    out["F"], out["F_s_by_cell"] = sorted(set(df["F"])), df.groupby("cell_id")["F_s"].first().to_dict()
    out["status_counts"] = dict(Counter(df["status"]))
    out["providers"] = dict(Counter(df["provider"]))
    return out


if __name__ == "__main__":
    main()
