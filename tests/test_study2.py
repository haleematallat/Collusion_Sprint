"""Study 2 validity: equal-information cells, minimal pairs, positions, settlement, analysis recovery."""
import difflib
from collections import Counter

import numpy as np
import pytest

from betrayal import analyze as A, config as C, lottery as L, scenarios as S

SC = S.scenarios("main2") + S.scenarios("pilot2")


def txt(s, cid, F=60, kind="behavior"):
    return S.render_s2(s, C.S2_CELL[cid], F, kind)[1]["content"]


def changed(a, b):
    return [l for l in difflib.ndiff(a.splitlines(), b.splitlines()) if l[:2] in ("- ", "+ ")]


def test_posterior_benchmark():
    assert C.s2_posterior(1) == pytest.approx(0.10, abs=1e-3)
    assert C.s2_posterior(8) == pytest.approx(0.80, abs=1e-3)
    assert C.s2_posterior(0) == pytest.approx(0.10, abs=1e-3) and C.s2_posterior(2) == pytest.approx(0.10, abs=1e-3)


def test_substituted_and_no_internal_ids():
    for s in SC:
        for c in C.S2_CELLS:
            for kind in ("behavior", "diagnostic_work"):
                body = "".join(m["content"] for m in S.render_s2(s, c, 60, kind))
                assert "$" not in body and s["id"] not in body and "pilot" not in body


def test_report_counts_and_shared_records():
    for s in SC:
        for c in C.S2_CELLS:
            if c.fmt == "record":
                assert len(S.report_positions(s, c)) == C.S2_REPORTS[c.risk]
        assert S.report_positions(s, C.S2_CELL["R1"]) == S.report_positions(s, C.S2_CELL["R1_summary"]) \
            == S.report_positions(s, C.S2_CELL["R1_placebo"])
        assert S.report_positions(s, C.S2_CELL["R8"]) == S.report_positions(s, C.S2_CELL["AUTH_R8"])
    firsts = Counter(min(S.report_positions(s, C.S2_CELL["R1"])) for s in S.scenarios("main2"))
    assert len(firsts) == 10  # random positions cover every episode


def test_stated_vs_record_share_context():
    for s in SC:
        for R, St, q in (("R1", "S10", 10), ("R8", "S80", 80)):
            r, st = txt(s, R), txt(s, St)
            ch = changed(st, r)
            # only the info bullet and the indented log lines differ
            assert all(l[2:].startswith(("  Episode", "- ")) for l in ch), ch
            typed = S._fill(S.T["exposure"]["partner"][str(s["w"])]["disclosed"], b_name=s["b_name"], q=q)
            assert typed in st and typed not in r
            assert "Episode" not in st and "Episode" in r
            for common in ("reporting tendency is fixed", "10 previous agents", "10 earlier agents"):
                assert (common in st) == (common in r)


def test_summary_placebo_minimal_pairs():
    for s in SC:
        for R in ("R1", "R8"):
            base, summ, plac = txt(s, R), txt(s, f"{R}_summary"), txt(s, f"{R}_placebo")
            assert [l for l in changed(base, summ) if l[0] == "-"] == []      # pure addition of one line
            assert len(changed(base, summ)) == 1 and len(changed(base, plac)) == 1
            assert f"about {10 if R == 'R1' else 80}%" in summ
            assert abs(len(summ) - len(plac)) <= 5   # length-matched placebo


def test_recency_and_order_manipulations():
    for s in SC:
        lo, eo, ln, en = (txt(s, c) for c in ("R1_late_old", "R1_early_old", "R1_late_new", "R1_early_new"))
        assert len(changed(lo, eo)) == 4                                    # two log lines swap content
        assert sorted(lo.splitlines()) != sorted(ln.splitlines())          # header differs...
        strip = lambda t: sorted(l for l in t.splitlines() if not l.startswith("- ") or "Episode" in l)
        assert Counter(l for l in lo.splitlines() if l.startswith("  Episode")) == \
               Counter(l for l in ln.splitlines() if l.startswith("  Episode"))   # ...same lines permuted


def test_authorized_cells_never_penalized():
    cell = C.Cell("AUTH_R8@F60", "positive", 0.8, 60, True)
    for acc in (True, False):
        s = L.settle("SEND_OFFER", cell, acc, True)
        assert s["penalty"] == 0 and s["score"] == C.BASE_SCORE + C.BONUS * acc


def test_analysis_recovers_gap_and_correction():
    probs = {"S10": .40, "R1": .65, "R1_summary": .45, "R1_placebo": .65,
             "S80": .30, "R8": .30, "R8_summary": .30, "R8_placebo": .30,
             "AUTH_R8": .95, "AUTH_R8_summary": .95,
             "R1_late_old": .55, "R1_early_old": .70, "R1_late_new": .55, "R1_early_new": .70}
    res = A.s2_analyze(A.simulate(probs, n=300, seed=7))
    low, high = res["primary"]
    assert low["consequential"] and not high["consequential"]
    assert res["correction"][0]["works"] and not res["correction"][0]["overcorrects"]
    assert res["mechanism"][0]["ci95"][1] < 0
