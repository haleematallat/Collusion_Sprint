"""Figures for the report: primary source comparison and the partner factorial."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from .analyze import wilson  # noqa: E402


def _rate(df, cid, w=None):
    g = df[(df["cell_id"] == cid) & (df["rep"] == 0)]
    if w is not None:
        g = g[g["w"] == w]
    y = g["y"].dropna()
    return (y.mean(), *wilson(int(y.sum()), len(y))) if len(y) else (np.nan, np.nan, np.nan)


def _bars(ax, groups, series, df):
    """groups: x labels; series: [(label, [cell per group], kwargs)]"""
    x, width = np.arange(len(groups)), 0.8 / len(series)
    for k, (lab, cells, kw) in enumerate(series):
        r = np.array([_rate(df, *c) if isinstance(c, tuple) else _rate(df, c) for c in cells])
        ax.bar(x + (k - (len(series) - 1) / 2) * width, r[:, 0], width, label=lab,
               yerr=[r[:, 0] - r[:, 1], r[:, 2] - r[:, 0]], capsize=3, **kw)
    ax.set_xticks(x, groups)
    ax.set_ylim(0, 1)
    ax.set_ylabel("P(SEND_OFFER)")
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2)


def plot_all(df, res, out):
    plt.style.use("seaborn-v0_8-whitegrid")
    qf = [(10, 0), (10, 20), (80, 0), (80, 20)]
    groups = [f"q={q}%\nF={F}" for q, F in qf]

    fig, ax = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
    _bars(ax[0], groups, [("partner reports", [f"partner_D_q{q}_F{F}" for q, F in qf], {"color": "#4C72B0"}),
                          ("automated audit", [f"audit_D_q{q}_F{F}" for q, F in qf], {"color": "#DD8452"})], df)
    ax[0].set_title("Exposure source (disclosed risk)")
    _bars(ax[1], ["wording 1", "wording 2"], [
        ("partner, q=80% F=20", [("partner_D_q80_F20", w) for w in (1, 2)], {"color": "#4C72B0"}),
        ("audit, q=80% F=20", [("audit_D_q80_F20", w) for w in (1, 2)], {"color": "#DD8452"})], df)
    pr = res["primary"]
    if "est" in pr:
        ax[1].set_title(f"Primary contrast by wording (pooled {pr['est']:+.2f}, 95% CI {pr['ci95'][0]:+.2f} to {pr['ci95'][1]:+.2f})", fontsize=9)
    fig.tight_layout()
    fig.savefig(out / "fig_source.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 3.6))
    _bars(ax, groups, [("risk disclosed", [f"partner_D_q{q}_F{F}" for q, F in qf], {"color": "#4C72B0"}),
                       ("risk undisclosed (45% mixture)", [f"partner_U_q{q}_F{F}" for q, F in qf], {"color": "#8C8C8C"})], df)
    ax.set_title("Partner arm: offer rate by true q, penalty F, disclosure", fontsize=9)
    fig.tight_layout()
    fig.savefig(out / "fig_factorial.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_calibration(diag, out):
    """diag: {"answer-only": rows, "with working": rows} from analyze_diagnostic."""
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    cells = [r["cell"] for r in next(iter(diag.values()))]
    x = np.arange(len(cells))
    for k, (fmt, rows) in enumerate(diag.items()):
        r = {d["cell"]: d for d in rows}
        m = np.array([r[c]["mean_p"] if c in r else np.nan for c in cells])
        e = np.array([(r[c]["err_ci95"][1] - r[c]["err_ci95"][0]) / 2 if c in r and r[c]["err_ci95"] else 0 for c in cells])
        ax.errorbar(x + (k - 0.5) * 0.25, m, yerr=e, fmt="o", capsize=3, label=fmt)
    ax.scatter(x, [next(iter(diag.values()))[i]["correct_p"] for i in range(len(cells))], marker="_", s=300, c="k", label="correct")
    ax.set_xticks(x, [c.replace("_", " ") for c in cells], rotation=60, ha="right", fontsize=7)
    ax.set_ylabel("forecast P(deduction applied)")
    ax.set_ylim(0, 1)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "fig_calibration.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_models(dfs, out):
    """dfs: {model label: behavior DataFrame}. Partner vs audit in the 4 matched disclosed cells, per model."""
    plt.style.use("seaborn-v0_8-whitegrid")
    qf = [(10, 0), (10, 20), (80, 0), (80, 20)]
    groups = [f"q={q}%\nF={F}" for q, F in qf]
    fig, ax = plt.subplots(1, len(dfs), figsize=(5 * len(dfs), 3.6), sharey=True)
    for a, (name, df) in zip(np.atleast_1d(ax), dfs.items()):
        _bars(a, groups, [("partner may report", [f"partner_D_q{q}_F{F}" for q, F in qf], {"color": "#4C72B0"}),
                          ("automated audit may detect", [f"audit_D_q{q}_F{F}" for q, F in qf], {"color": "#DD8452"})], df)
        a.set_title(name, fontsize=10)
    fig.tight_layout()
    fig.savefig(out / "fig_source_models.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_s2(dfs, out):
    """Study 2: stated vs record (alone, + calibrated summary, + placebo) at low and high risk, per model."""
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(1, len(dfs), figsize=(4.6 * len(dfs), 3.8), sharey=True)
    series = [("stated rate", "S{}", "#8C8C8C"), ("record", "R{}", "#4C72B0"),
              ("record + calibrated summary", "R{}_summary", "#55A868"), ("record + placebo", "R{}_placebo", "#C44E52")]
    for a, (name, df) in zip(np.atleast_1d(ax), dfs.items()):
        _bars(a, ["low risk\n(10%; 1 of 10)", "high risk\n(80%; 8 of 10)"],
              [(lab, [pat.format(k) if pat[0] == "R" else pat.format(q) for k, q in ((1, 10), (8, 80))], {"color": col})
               for lab, pat, col in series], df)
        a.set_title(name, fontsize=10)
    fig.tight_layout()
    fig.savefig(out / "fig_s2_format.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_s3b(frames, out):
    """Study 3b: per model and cell, send rate and operator-visible reports (top) vs completed misconduct (bottom)."""
    cells = ["E", "L", "LOW", "HIGH"]
    fig, ax = plt.subplots(2, len(frames), figsize=(4.2 * len(frames), 5.2), sharex=True, squeeze=False)
    for j, (name, d) in enumerate(frames.items()):
        g = d[d["cell"].isin(cells)].groupby("cell")
        m, se = g[["P", "t1", "cum"]].mean().reindex(cells), g[["P", "t1", "cum"]].sem().reindex(cells)
        x = np.arange(len(cells))
        for k, (col, lab, c) in enumerate((("P", "sends proposal", "#888888"), ("t1", "expected reports", "#3b6ea8"))):
            ax[0, j].bar(x + (k - 0.5) * 0.38, m[col], 0.38, yerr=1.96 * se[col], color=c, label=lab, capsize=2)
        ax[1, j].bar(x, m["cum"], 0.5, yerr=1.96 * se["cum"], color="#c0504d", capsize=2, label="expected simulated completed misconduct")
        ax[0, j].set_title(name)
        ax[0, j].set_ylim(0, 1.05)
        ax[1, j].set_xticks(x, ["E\nold", "L\nrecent", "LOW\n1/10", "HIGH\n8/10"])
    ax[0, 0].set_ylabel("rate per trial")
    ax[1, 0].set_ylabel("expected CUM per trial")
    h0, l0 = ax[0, 0].get_legend_handles_labels()
    h1, l1 = ax[1, 0].get_legend_handles_labels()
    fig.legend(h0 + h1, l0 + l1, loc="lower center", ncol=3, frameon=False)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(out, dpi=150)
    plt.close(fig)


def plot_recency(dfs, out):
    """Study 2: one report in the oldest vs the most recent episode, under each listing order, per model."""
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(1, len(dfs), figsize=(4.2 * len(dfs), 3.6), sharey=True)
    for a, (name, df) in zip(np.atleast_1d(ax), dfs.items()):
        _bars(a, ["listed\noldest-first", "listed\nmost-recent-first"],
              [("single report in the oldest episode", ["R1_early_old", "R1_early_new"], {"color": "#8C8C8C"}),
               ("single report in the most recent episode", ["R1_late_old", "R1_late_new"], {"color": "#C44E52"})], df)
        a.set_title(name, fontsize=10)
        a.get_legend().remove()
    fig.legend(*np.atleast_1d(ax)[0].get_legend_handles_labels(), frameon=False, fontsize=9, ncol=2,
               loc="lower center", bbox_to_anchor=(0.5, -0.08))
    fig.tight_layout()
    fig.savefig(out / "fig_s2_recency.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


OVERVIEW = [  # (label, phase, path to the saved contrast in summary_no_offer.json)
    ("Penalty 0 \u2192 20, partner reports (80% risk)", "main", ("behavior", "secondary", "F effect, partner D q=.8")),
    ("Penalty 0 \u2192 20, audit detects (80% risk)", "main", ("behavior", "descriptive", "F effect, audit D q=.8")),
    ("Partner \u2212 audit (80% risk, F = 20)", "main", ("behavior", "primary", None)),
    ("Partner \u2212 audit (80% risk, F = 0)", "main", ("behavior", "generalization", "partner - audit (D, q=.8, F=0)")),
    ("Record \u2212 stated rate (10% risk)", "main2", ("study2", "primary", "format gap low: R1 - S10")),
    ("Record \u2212 stated rate (80% risk)", "main2", ("study2", "primary", "format gap high: R8 - S80")),
    ("Recent \u2212 old single report", "main2", ("study2", "mechanism", "recency (late - early), pooled over list order")),
]
MODELS = {"DeepSeek-V3.2": ("deepseek__deepseek-v3.2", "#4C72B0"), "GPT-4.1-mini": ("openai__gpt-4.1-mini", "#DD8452"),
          "Llama-3.3-70B": ("meta-llama__llama-3.3-70b-instruct", "#55A868")}


def plot_overview(root, out):
    """Headline: each presentation contrast next to the penalty effect, per model (saved paired estimates, 95% CIs)."""
    import json
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    for k, (name, (slug, col)) in enumerate(MODELS.items()):
        for i, (_, phase, (top, fam, rname)) in enumerate(OVERVIEW):
            f = root / "results" / phase / slug / "summary_no_offer.json"
            if not f.exists():
                continue   # Llama was not run in Block 1
            sec = json.loads(f.read_text())[top][fam]
            r = sec if rname is None else next(x for x in sec if x["name"] == rname)
            y = i + (k - 1) * 0.22
            ax.errorbar(100 * r["est"], y, xerr=[[100 * (r["est"] - r["ci95"][0])], [100 * (r["ci95"][1] - r["est"])]],
                        fmt="o", color=col, ms=4, capsize=2)
        ax.plot([], [], "o", color=col, label=name)
    ax.axvline(0, color="black", lw=0.8)
    ax.axhline(1.5, color="#999999", lw=0.6, ls="--")
    ax.set_yticks(range(len(OVERVIEW)), [o[0] for o in OVERVIEW], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("change in offer rate (percentage points), 95% CI", fontsize=9)
    ax.set_xlim(-80, 45)
    ax.legend(frameon=False, fontsize=8, ncol=3, loc="lower center", bbox_to_anchor=(0.5, 1.0))
    fig.tight_layout()
    fig.savefig(out / "fig_overview.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":   # regenerate every report figure from the raw logs and saved summaries
    import json
    from .analyze import ROOT, load, s3b_frame
    res = ROOT / "results"
    names = {m: n for n, (m, _) in MODELS.items()}
    b1 = {n + (" (primary)" if "deepseek" in m else " (replication)"): load(ROOT / "data/main" / m / "behavior.jsonl")
          for m, n in names.items() if (ROOT / "data/main" / m).exists()}
    b2 = {n: load(ROOT / "data/main2" / m / "behavior.jsonl") for m, n in names.items()}
    b3 = {n: s3b_frame(load(ROOT / "data/main3b" / m / "behavior.jsonl"),
                       [json.loads(l) for l in open(ROOT / "data/main3b" / m / "reporter_scores.jsonl")])
          for m, n in names.items() if (ROOT / "data/main3b" / m).exists()}
    plot_overview(ROOT, res)
    plot_models(b1, res / "main")
    plot_s2(b2, res / "main2")
    plot_recency(b2, res / "main2")
    plot_s3b(b3, res / "main3b" / "fig_s3b.png")
