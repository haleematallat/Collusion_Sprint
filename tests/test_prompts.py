"""Validity checks B (no leakage of hidden type) and D (partner vs audit differ only in the exposure source)."""
import difflib
import re
from collections import Counter

from betrayal import config as C, scenarios as S

ALL = S.scenarios("main") + S.scenarios("pilot")


def txt(s, cid, kind="behavior"):
    return S.render(s, C.CELL[cid], kind)[1]["content"]


def test_fully_substituted_and_no_internal_ids():
    for s in ALL:
        for c in C.CELLS:
            for kind in ("behavior", "diagnostic"):
                m = S.render(s, c, kind)
                body = m[0]["content"] + m[1]["content"]
                assert "$" not in body
                assert s["id"] not in body and "pilot" not in body and "main-" not in body
                assert "45%" not in body  # the mixture answer is never given


def test_undisclosed_prompts_identical_across_hidden_type():
    for s in ALL:
        for F in C.F_LEVELS:
            for kind in ("behavior", "diagnostic"):
                assert txt(s, f"partner_U_q10_F{F}", kind) == txt(s, f"partner_U_q80_F{F}", kind)
        flipped = dict(s, hidden_q=C.Q_LOW if s["hidden_q"] == C.Q_HIGH else C.Q_HIGH)
        assert txt(s, "neutral_U_F20") == txt(flipped, "neutral_U_F20")


def test_disclosure_content():
    for s in ALL:
        e = S.T["exposure"]["partner"][str(s["w"])]
        for q in (10, 80):
            d = txt(s, f"partner_D_q{q}_F20")
            assert S._fill(e["disclosed"], b_name=s["b_name"], q=q) in d
            assert S._fill(e["disclosed"], b_name=s["b_name"], q=90 - q) not in d
        u = txt(s, "partner_U_q10_F20")
        assert S._fill(e["undisclosed"], b_name=s["b_name"]) in u
        for t in (u, txt(s, "partner_D_q80_F20")):
            assert "10%" in t and "80%" in t  # population mixture always stated


def _changed(a, b):
    return [l[2:] for l in difflib.ndiff(a.splitlines(), b.splitlines()) if l[:2] in ("- ", "+ ")]


def test_partner_vs_audit_differ_only_in_source_lines():
    for s in ALL:
        for q in (10, 80):
            for F in C.F_LEVELS:
                p, a = txt(s, f"partner_D_q{q}_F{F}"), txt(s, f"audit_D_q{q}_F{F}")
                changed = _changed(p, a)
                assert changed and all(l.startswith("- ") for l in changed), changed
                pb = [l for l in changed if l in p.splitlines()]
                ab = [l for l in changed if l in a.splitlines()]
                # same numbers (q, F, bonus, mixture rates) on both sides
                assert Counter(re.findall(r"\d+%?", " ".join(pb))) == Counter(re.findall(r"\d+%?", " ".join(ab)))
                # identical decision section / options
                assert p.split("DECISION")[1] == a.split("DECISION")[1]
                assert f"{q}%" in " ".join(pb) and f"{q}%" in " ".join(ab)
                assert p.count(f"{F} points") == a.count(f"{F} points") >= 1


def test_neutral_vs_undisclosed_differ_only_in_info_sentence():
    for s in ALL:
        e = S.T["exposure"]["partner"][str(s["w"])]
        n_, u_ = txt(s, "neutral_U_F20"), txt(s, "partner_U_q10_F20")
        und = S._fill(e["undisclosed"], b_name=s["b_name"])
        assert n_ == u_.replace(und, und + " " + S._fill(e["neutral"], b_name=s["b_name"]))


def test_wording_balanced_and_deterministic():
    for phase in ("main", "pilot"):
        sc = S.scenarios(phase)
        assert Counter(s["w"] for s in sc) == {1: len(sc) // 2, 2: len(sc) // 2}
        again = S.scenarios(phase)
        assert [S.prompt_hash(S.render(s, C.CELL[c], "behavior")) for s in sc for c in C.CORE] == \
               [S.prompt_hash(S.render(s, C.CELL[c], "behavior")) for s in again for c in C.CORE]
    assert len({(s["org"], s["task"], s["a_name"], s["b_name"]) for s in ALL}) == len(ALL)
    for phase in ("main", "pilot"):
        sc = S.scenarios(phase)
        cells = Counter((s["w"], s["send_first"]) for s in sc)
        assert set(cells.values()) == {len(sc) // 4} and len(cells) == 4, cells
