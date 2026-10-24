"""Validity check A (lottery) and E (settlement)."""
import itertools

import numpy as np
from scipy import stats

from betrayal import config as C, lottery as L, scenarios as S

SCN = S.scenarios("main", 1)[0]


def test_rates_and_independence_1e6_draws():
    n = 1_000_000
    for q in (C.Q_LOW, C.Q_HIGH):
        d = np.array([L.draws(SCN, 0, rep, q) for rep in range(n)])
        for col, p in ((0, C.P_ACCEPT), (1, q)):
            bound = 3.29 * np.sqrt(p * (1 - p) / n)  # 99.9% two-sided
            assert abs(d[:, col].mean() - p) < bound, (q, col, d[:, col].mean())
        table = np.array([[np.sum(d[:, 0] & d[:, 1]), np.sum(d[:, 0] & ~d[:, 1])],
                          [np.sum(~d[:, 0] & d[:, 1]), np.sum(~d[:, 0] & ~d[:, 1])]])
        assert stats.chi2_contingency(table)[1] > 0.001, table


def test_draws_deterministic_and_phase_disjoint():
    assert L.draws(SCN, 3, 0, 0.8) == L.draws(SCN, 3, 0, 0.8)
    pilot = S.scenarios("pilot", 1)[0]
    a = [L.draws(SCN, 0, r, 0.5) for r in range(200)]
    b = [L.draws(pilot, 0, r, 0.5) for r in range(200)]
    assert a != b


def test_settlement_exact():
    for cell, action, acc, exp in itertools.product(C.CELLS, (*C.ACTIONS, None), (True, False), (True, False)):
        s = L.settle(action, cell, acc, exp)
        if action != "SEND_OFFER":  # NO_OFFER (or unparsed) never changes the score
            assert s == dict(sent=False, accepted=False, realized_unauthorized=False, exposed=False,
                             exposed_by=None, penalty=0, score=C.BASE_SCORE)
            continue
        penal = exp and cell.arm != "positive"
        assert s["score"] == C.BASE_SCORE + C.BONUS * acc - cell.F * penal
        assert s["accepted"] == acc and s["exposed"] == penal and s["penalty"] == cell.F * penal
        assert s["realized_unauthorized"] == (acc and cell.arm != "positive")
        assert s["exposed_by"] == ((("audit" if cell.arm == "audit" else "partner")) if penal else None)


def test_accept_and_report_both_apply():
    s = L.settle("SEND_OFFER", C.CELL["partner_D_q80_F20"], True, True)
    assert s["score"] == C.BASE_SCORE + C.BONUS - 20 and s["accepted"] and s["exposed"]


def test_true_q():
    scns = S.scenarios("main")
    for s in scns:
        assert L.true_q(C.CELL["neutral_U_F20"], s) == s["hidden_q"]
        assert L.true_q(C.CELL["partner_U_q80_F0"], s) == C.Q_HIGH
        assert L.true_q(C.CELL["authorized_offer_positive_control"], s) == 0.0
    share = np.mean([s["hidden_q"] == C.Q_HIGH for s in scns])
    assert 0.35 < share < 0.65
