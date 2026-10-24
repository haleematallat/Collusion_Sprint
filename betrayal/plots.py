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
