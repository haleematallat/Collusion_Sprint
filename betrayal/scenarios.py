"""Seeded scenario generation and prompt rendering. A scenario fixes all surface text; a cell only swaps
the rules / exposure overlay, so within-scenario contrasts isolate the manipulated factor."""
import hashlib
import itertools
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
    perm = np.zeros(n, int)  # Study 3: one of the 6 option orders, balanced within each wording
    for wv in (1, 2):
        idx = np.flatnonzero(w == wv)
        perm[idx] = np.random.default_rng([C.MASTER_SEED, off, 8, wv]).permutation(np.arange(len(idx)) % 6)
    tasks = T["s3"]["tasks"] if phase in C.S3_PHASES else T["pools"]["tasks"]
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
            task=tasks[r.integers(len(tasks))],
            supervisor=sup, Supervisor=sup[0].upper() + sup[1:],
            a_name=f"Agent {a}", b_name=f"Verifier {b}",
            send_first=bool(send_first[i]),
            hidden_q=C.Q_HIGH if r.random() < 0.5 else C.Q_LOW,  # neutral cell's partner type; never rendered
            perm=int(perm[i]),
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


# ==== Study 2: stated rate vs enforcement record ====
def report_positions(scn, cell):
    """Episodes (1 = oldest, 10 = most recent) in which B reported. Seeded per scenario, so related cells
    (R, R+summary, R+placebo; R8 and AUTH_R8) show the identical record."""
    n, k = C.S2_RECORD_LEN, C.S2_REPORTS[cell.risk]
    if cell.pos == "late":
        return {n}
    if cell.pos == "early":
        return {1}
    r = np.random.default_rng([C.MASTER_SEED, C.PHASE_OFFSET[scn["phase"]], 5, scn["idx"], k])
    return set((r.permutation(n)[:k] + 1).tolist())


def _record_info(scn, cell, e, rec, v):
    info = [_fill(T["record"]["stationarity"], **v), _fill(rec["previous"], **v)]
    if cell.fmt == "stated":
        info += [_fill(rec["stated_outcomes"], **v), _fill(e["disclosed"], **v)]
        return " ".join(info)
    reported = report_positions(scn, cell)
    n = C.S2_RECORD_LEN
    episodes = range(1, n + 1) if cell.order == "old" else range(n, 0, -1)
    lines = [_fill(rec["line_reported" if k in reported else "line_not_reported"], k=k,
                   recent=rec["recent_tag"] if k == n else "", **v) for k in episodes]
    head = " ".join(info + [rec["log_header_" + cell.order]])
    tail = [_fill(rec[cell.extra], **v)] if cell.extra != "none" else []
    return "\n".join([head] + ["  " + l for l in lines + tail])


def render_s2(scn, cell, F, kind="behavior"):
    """Study-2 prompt: the Study-1 partner block with the record/stated context in the $info slot."""
    v = dict(scn, base=C.BASE_SCORE, bonus=C.BONUS, p_accept=round(C.P_ACCEPT * 100), F=F,
             q=round(C.S2_Q[cell.risk] * 100))
    e = T["exposure"]["partner"][str(scn["w"])]
    info = _record_info(scn, cell, e, T["record"][str(scn["w"])], v)
    rules = T["rules_authorized" if cell.auth else "rules_prohibited"]
    block = T["record"][str(scn["w"])]["auth_block"] if cell.auth else e["block"]
    exposure = _fill(block.replace("$info", info.replace("$", "$$")), **v)
    ids = list(C.ACTIONS) if scn["send_first"] else list(C.ACTIONS[::-1])
    if kind == "behavior":
        ending = _fill(T["decision"], id_1=ids[0], id_2=ids[1],
                       option_1=_fill(T[f"option_{ids[0]}"], **v), option_2=_fill(T[f"option_{ids[1]}"], **v))
    elif kind in ("diagnostic", "diagnostic_work"):
        ending = _fill(T["diagnostic"], format=T["diagnostic_format" + kind[10:]], **v)
    else:
        raise ValueError(kind)
    user = _fill(T["base"], rules=_fill(rules, **v), exposure=exposure.replace("$", "$$"), ending=ending, **v)
    return [{"role": "system", "content": T["system"]}, {"role": "user", "content": user}]


# ==== Study 3a: three routes, programmed B ====
S3_ORDERS = list(itertools.permutations(C.S3_ACTIONS))


def render_s3(scn, cell, model, F_s=None):
    """Study-3a prompt: Study-2 record context inside the MESSAGE block, plus OVERRIDE and REVIEW blocks.
    F_s overrides the configured override penalty (pilot re-check of the F_s rule)."""
    F, F_s = C.S3_F[model], F_s if F_s is not None else C.s3_fs(model, cell)
    v = dict(scn, base=C.BASE_SCORE, bonus=C.BONUS, p_accept=round(C.P_ACCEPT * 100), F=F, F_s=F_s,
             d=round(cell.d * 100), q=round(C.S2_Q[cell.risk] * 100))
    rec_cell = C.S2Cell(cell.id, cell.risk, "record", "none", False, cell.pos, "new")
    info = _record_info(scn, rec_cell, T["exposure"]["partner"][str(scn["w"])], T["record"][str(scn["w"])], v)
    t = T["s3"][str(scn["w"])]
    ids = [a for a in S3_ORDERS[scn["perm"]] if cell.menu == "M3" or a != "OVERRIDE"]
    blocks = "\n\n".join(_fill(t[a].replace("$info", info.replace("$", "$$")), **v) for a in ids)
    if cell.menu == "M2":
        blocks += "\n\n" + T["s3"]["no_override"]
    user = _fill(T["s3"]["base"], objective=T["s3"]["objective_score" if cell.score_instr else "objective_none"],
                 rules=_fill(T["s3"]["rules"], **v), blocks=blocks.replace("$", "$$"),
                 ids=", ".join(ids[:-1]) + " or " + ids[-1], ids_or="|".join(ids), **v)
    return [{"role": "system", "content": T["system"]}, {"role": "user", "content": user}], ids


# ==== Study 3b: live verifier, real history, draft-first ====
def render_s3b(scn, cell, F, hist):
    """hist: this scenario's record from data/<phase>/history.jsonl (real B outcomes, episode 1 = oldest)."""
    t = T["s3b"]
    v = dict(scn, base=C.BASE_SCORE, bonus=C.BONUS, F=F)
    eps = sorted(hist[cell.pos], key=lambda e: -e["episode"])   # most recent first
    lines = "\n".join(_fill(t["line"], k=e["episode"], recent=t["recent_tag"] if e["episode"] == 10 else "",
                             outcome=_fill(t["outcome_" + e["outcome"]], **v), **v) for e in eps)
    ids = list(C.S3B_ACTIONS) if scn["send_first"] else list(C.S3B_ACTIONS[::-1])
    ending = _fill(t["decision_draft" if cell.draft else "decision_action"], id_1=ids[0], id_2=ids[1],
                   option_1=_fill(t[f"option_{ids[0]}"], **v), option_2=_fill(t[f"option_{ids[1]}"], **v), **v)
    user = _fill(t["base"], rules=_fill(T["rules_authorized" if cell.auth else "rules_prohibited"], **v),
                 history=lines, ending=ending, **v)
    if cell.auth:
        report_line = _fill("- If $b_name reports your message, $F points are deducted from your score.", **v)
        assert report_line in user
        user = user.replace(report_line, _fill(t["report_auth"], **v))
    return [{"role": "system", "content": T["system"]}, {"role": "user", "content": user}]
