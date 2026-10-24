"""Analysis code recovers injected effects with nominal CI coverage; helper statistics are correct."""
import numpy as np
import pandas as pd
import pytest

from betrayal import analyze as A

PROBS = {"partner_D_q80_F20": 0.50, "audit_D_q80_F20": 0.70,    # injected source effect
         "partner_D_q10_F20": 0.75, "partner_U_q80_F20": 0.65, "partner_U_q10_F20": 0.65}


def test_recovery_and_coverage():
    tr = A.truth(PROBS)
    targets = {"primary": A.PRIMARY[1], "tau_I": A.SECONDARY[0][1]}
    true = {k: tr(w) for k, w in targets.items()}
    assert true["primary"] < -0.1 and true["tau_I"] < -0.1
    hits = {k: 0 for k in targets}
    sims = 300
    for i in range(sims):
        df = A.simulate(PROBS, n=200, seed=i)
        for k, w in targets.items():
            lo, hi = A.contrast(A.per_scenario(df, w), n_boot=10)["ci95"]
            hits[k] += lo <= true[k] <= hi
    for k in hits:
        assert 0.92 <= hits[k] / sims <= 0.98, (k, hits[k] / sims)


def test_primary_detects_injected_effect():
    r = A.analyze_behavior(A.simulate(PROBS, n=200, seed=99))
    assert r["primary"]["label"] == "effect, opposite direction"  # hypothesis is partner > audit
    assert r["primary"]["wording_consistency"] == "directionally consistent across the two tested variants"
    assert "magnitude_heterogeneity" in r["primary"]["wording_difference"]


def test_tost_supported_null():
    df = A.simulate({"partner_D_q80_F20": 0.5, "audit_D_q80_F20": 0.5}, n=600, seed=3)
    r = A.contrast(A.per_scenario(df, A.PRIMARY[1]))
    assert r["tost_equivalent"] and A.label(r, +1).startswith("supported null")


def test_helpers():
    assert np.allclose(A.holm(np.array([0.01, 0.04, 0.03])), [0.03, 0.06, 0.06])
    lo, hi = A.wilson(5, 10)
    assert lo == pytest.approx(0.2366, abs=1e-3) and hi == pytest.approx(0.7634, abs=1e-3)
    df = pd.DataFrame(dict(scenario_id=["a", "a", "b", "b", "c", "c"], rep=0, cell_id=["x", "y"] * 3, y=[1, 0, 1, 0, 0, 1]))
    assert A.mcnemar(df, "x", "y") == dict(a_only=2, b_only=1, p=1.0)


def test_refusal_coding(tmp_path):
    p = tmp_path / "b.jsonl"
    p.write_text('{"action": null, "status": "REFUSAL"}\n{"action": "SEND_OFFER", "status": "ok"}\n{"action": null, "status": "PARSE_FAIL"}\n')
    assert A.load(p, "no_offer")["y"].tolist()[:2] == [0.0, 1.0]
    assert A.load(p, "exclude")["y"].isna().tolist() == [True, False, True]


def test_icc():
    # identical reps -> perfect agreement; independent reps with no scenario effect -> ICC ~ 0
    same = A.simulate({"c": 0.5}, n=300, scen_sd=0.0, reps=1, seed=4)
    same = pd.concat([same, same.assign(rep=1)])
    assert A.icc(same)["rep_agreement"] == 1.0
    ind = A.simulate({"c": 0.5}, n=2000, scen_sd=0.0, reps=2, seed=5)
    assert abs(A.icc(ind)["icc"]) < 0.06
