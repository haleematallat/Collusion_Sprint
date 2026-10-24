"""Seeded scenario generation and prompt rendering. A scenario fixes all surface text; a cell only swaps
the rules / exposure overlay, so within-scenario contrasts isolate the manipulated factor."""
import hashlib
import tomllib
from pathlib import Path
from string import Template

import numpy as np

from . import config as C

T = tomllib.loads((Path(__file__).parent.parent / "prompts" / "templates.toml").read_text())


def _code(r):
    return f"{chr(65 + r.integers(26))}{chr(65 + r.integers(26))}-{r.integers(100, 1000)}"


def scenarios(phase, n=None):
    """The phase's scenarios; n takes the first n. Assignments are always balanced over the full phase,
    so a subset (e.g. rep 2 on scenarios 0-39) gets exactly the same wording and order as the full run."""
    full = C.N_SCENARIOS[phase]
    assert n is None or n <= full, n
    return _scenarios(phase, full)[:n]


def _scenarios(phase, n):
    off = C.PHASE_OFFSET[phase]
    w = np.random.default_rng([C.MASTER_SEED, off, 0]).permutation(np.arange(n) % 2) + 1  # balanced wording
    send_first = np.zeros(n, bool)  # action order balanced within each wording, so independent of it
    for wv in (1, 2):
        idx = np.flatnonzero(w == wv)
        send_first[idx] = np.random.default_rng([C.MASTER_SEED, off, 4, wv]).permutation(np.arange(len(idx)) % 2) == 0
    out = []
    for i in range(n):
        r = np.random.default_rng([C.MASTER_SEED, off, 1, i])
        a, b = _code(r), _code(r)
        while b == a:
            b = _code(r)
        sup = T["pools"]["supervisors"][r.integers(len(T["pools"]["supervisors"]))]
        out.append(dict(
            id=f"{phase}-{i:03d}", idx=i, phase=phase, w=int(w[i]),
            org=T["pools"]["orgs"][r.integers(len(T["pools"]["orgs"]))],
            task=T["pools"]["tasks"][r.integers(len(T["pools"]["tasks"]))],
            supervisor=sup, Supervisor=sup[0].upper() + sup[1:],
            a_name=f"Agent {a}", b_name=f"Verifier {b}",
            send_first=bool(send_first[i]),
            hidden_q=C.Q_HIGH if r.random() < 0.5 else C.Q_LOW,  # neutral cell's partner type; never rendered
        ))
    return out


def _fill(text, **kw):
    return Template(text).substitute(**kw)


def render(scn, cell, kind="behavior"):
    """Return the chat messages for one (scenario, cell). kind: behavior | diagnostic | diagnostic_work."""
    v = dict(scn, base=C.BASE_SCORE, bonus=C.BONUS, p_accept=round(C.P_ACCEPT * 100), F=cell.F)
    if cell.arm == "positive":
        rules, exposure = T["rules_authorized"], T["exposure"]["positive"]["block"]
    else:
        src = "audit" if cell.arm == "audit" else "partner"
        e = T["exposure"][src][str(scn["w"])]
        info = e["disclosed"] if cell.disclosed else e["undisclosed"]
        if cell.arm == "neutral":  # neutral metadata is added, never replaces "not told which type"
            info += " " + e["neutral"]
        rules = T["rules_prohibited"]
        exposure = e["block"].replace("$info", info)
        if cell.disclosed:
            v["q"] = round(cell.q * 100)
    ids = list(C.ACTIONS) if scn["send_first"] else list(C.ACTIONS[::-1])
    if kind == "behavior":
        ending = _fill(T["decision"], id_1=ids[0], id_2=ids[1],
                       option_1=_fill(T[f"option_{ids[0]}"], **v), option_2=_fill(T[f"option_{ids[1]}"], **v))
    elif kind in ("diagnostic", "diagnostic_work"):
        ending = _fill(T["diagnostic"], format=T["diagnostic_format" + kind[10:]], **v)
    else:
        raise ValueError(kind)
    user = _fill(T["base"], rules=_fill(rules, **v), exposure=_fill(exposure, **v), ending=ending, **v)
    return [{"role": "system", "content": T["system"]}, {"role": "user", "content": user}]


def prompt_hash(messages):
    return hashlib.sha256(repr(messages).encode()).hexdigest()[:16]
