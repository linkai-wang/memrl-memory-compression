"""Rebuild static result figures from public aggregate JSON; no model/API calls."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
BLUE, ORANGE, INK, MUTED = "#2874B2", "#E18436", "#172C40", "#62758A"
ARMS = ("A_full300", "C_content195")
TASKS = [
    ("pick_clean_then_place_in_recep", "Clean then place"),
    ("look_at_obj_in_light", "Look at object in light"),
    ("pick_cool_then_place_in_recep", "Cool then place"),
    ("pick_and_place_simple", "Simple pick and place"),
    ("pick_two_obj_and_place", "Place two objects"),
    ("pick_heat_then_place_in_recep", "Heat then place"),
]


def load_data():
    summary = json.loads((ROOT / "results/eval_summary.json").read_text(encoding="utf-8"))
    paired = json.loads((ROOT / "results/paired_analysis.json").read_text(encoding="utf-8"))
    if not (summary["complete"] is True and paired["complete"] is True
            and summary["paired"]["completed_pairs"] == paired["paired_tasks"] == 300):
        raise ValueError("Expected a complete 300-task paired evaluation")
    for arm, key in zip(ARMS, ("A_successes", "C_successes")):
        row = summary["arms"][arm]
        if row["completed"] != 300 or row["pending"] != 0:
            raise ValueError("Incomplete evaluation arm")
        if sum(t[key] for t in paired["by_task_type"].values()) != row["successes"]:
            raise ValueError("Task-type totals disagree with aggregate results")
        tokens = row["solver_usage"]
        if tokens["prompt_tokens"] + tokens["completion_tokens"] != tokens["total_tokens"]:
            raise ValueError("Token totals disagree")
    cells = paired["discordance_table"]
    if sum(cells.values()) != 300 or any(summary["paired"][key] != value for key, value in cells.items()):
        raise ValueError("Paired outcome tables disagree")
    return summary, paired


def style():
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 11, "axes.titlesize": 13,
        "axes.labelsize": 10, "text.color": INK, "axes.labelcolor": MUTED,
        "xtick.color": MUTED, "ytick.color": MUTED, "axes.edgecolor": "#DCE4EC",
        "axes.spines.top": False, "axes.spines.right": False,
        "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
        "svg.hashsalt": "memrl-ac300-2026-11-02", "svg.fonttype": "path",
    })


def save(fig, name):
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / (name + ".svg"), bbox_inches="tight", metadata={"Date": None})
    fig.savefig(OUT / (name + ".png"), dpi=170, bbox_inches="tight")
    plt.close(fig)


def legend(fig, y):
    fig.legend(handles=[Patch(color=BLUE, label="A: original 300"),
                        Patch(color=ORANGE, label="C: selected 195")],
               loc="upper center", bbox_to_anchor=(.5, y), ncol=2, frameon=False)


def overview(summary):
    a, c = (summary["arms"][arm] for arm in ARMS)
    panels = [
        ("Active memory records", [a["memory_count"], c["memory_count"]], "records", "35% fewer records", "{:.0f}", 350),
        ("Task success rate", [100*a["success_rate"], 100*c["success_rate"]], "%", "same observed success rate", "{:.2f}%", 112),
        ("Mean decisions per task", [a["mean_decisions"], c["mean_decisions"]], "decisions", "+4.66% observed in C", "{:.2f}", 17),
        ("Total solver tokens", [a["solver_usage"]["total_tokens"]/1e6, c["solver_usage"]["total_tokens"]/1e6], "million tokens", "+6.21% observed in C", "{:.2f}M", 26),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.5))
    fig.subplots_adjust(left=.09, right=.97, bottom=.13, top=.80, hspace=.48, wspace=.28)
    fig.suptitle("MemRL memory compression: first A/C comparison", x=.5, y=.98, fontsize=19, fontweight="bold")
    fig.text(.5, .93, "300 shared holdout tasks per group | same MemRL retrieval | memory and Q frozen",
             ha="center", color=MUTED, fontsize=10)
    legend(fig, .905)
    for ax, (title, values, unit, note, fmt, upper) in zip(axes.flat, panels):
        ax.set_title(title, loc="left", fontweight="bold", pad=12)
        ax.set_axisbelow(True)
        ax.grid(axis="y", color="#EBEFF4")
        bars = ax.bar([0, 1], values, width=.5, color=[BLUE, ORANGE])
        ax.set_xticks([0, 1], ["A", "C"])
        ax.set_ylim(0, upper)
        ax.set_ylabel(unit)
        ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
        ax.bar_label(bars, labels=[fmt.format(v) for v in values], padding=5, color=INK, fontsize=12, fontweight="bold")
        ax.text(.5, -.23, note, transform=ax.transAxes, ha="center", color=MUTED, fontsize=10)
    fig.text(.5, .025, "Bars show observed values. Decision/token difference intervals include zero; see the paired uncertainty figure.",
             ha="center", fontsize=9, color=MUTED)
    save(fig, "overview")


def task_types(paired):
    fig, ax = plt.subplots(figsize=(11.5, 6))
    fig.subplots_adjust(left=.25, right=.94, top=.78, bottom=.13)
    fig.suptitle("Success by task type", y=.97, fontsize=19, fontweight="bold")
    fig.text(.5, .91, "50 paired tasks per type | one model run per task and group", ha="center", color=MUTED)
    legend(fig, .88)
    ys = list(range(len(TASKS)))
    for offset, key, color in [(-.18, "A_successes", BLUE), (.18, "C_successes", ORANGE)]:
        values = [paired["by_task_type"][kind][key] for kind, _ in TASKS]
        bars = ax.barh([y+offset for y in ys], values, height=.31, color=color)
        ax.bar_label(bars, labels=[f"{v}/50" for v in values], padding=6, color=INK, fontsize=10)
    ax.set_yticks(ys, [label for _, label in TASKS])
    ax.invert_yaxis()
    ax.set_xlim(0, 57)
    ax.set_xticks([0, 10, 20, 30, 40, 50])
    ax.set_xlabel("Successful tasks (out of 50)")
    ax.set_axisbelow(True)
    ax.grid(axis="x", color="#EBEFF4")
    save(fig, "task_types")


def uncertainty(paired):
    specs = [
        ("Success rate", "success_difference_percentage_points", 1, "percentage points", (-3.1, 3.1), ".2f"),
        ("Decisions per task", "decision_steps_difference", 1, "decisions / task", (-.85, 2.15), ".3f"),
        ("Solver tokens per task", "solver_tokens_difference", .001, "thousand tokens / task", (-9.5, 18), ".2f"),
        ("Presented memory context", "memory_context_characters_difference", 1, "characters / task", (-12, 90), ".2f"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 6.8))
    fig.subplots_adjust(left=.09, right=.97, top=.78, bottom=.16, hspace=.72, wspace=.28)
    fig.suptitle("Paired differences and uncertainty", y=.97, fontsize=19, fontweight="bold")
    fig.text(.5, .91, "C minus A | point = observed difference | line = 95% paired bootstrap interval", ha="center", color=MUTED, fontsize=10)
    for ax, (title, key, scale, unit, limits, fmt) in zip(axes.flat, specs):
        row = paired["all_task_paired_differences"][key]
        estimate = row["C_minus_A"] * scale
        low, high = [v * scale for v in row["ci95"]]
        ax.set_title(title, loc="left", fontweight="bold", pad=10)
        ax.axvline(0, color="#A9B6C4", linestyle="--", linewidth=1.1)
        ax.errorbar(estimate, 0, xerr=[[estimate-low], [high-estimate]], fmt="o", markersize=8,
                    color=BLUE, ecolor=BLUE, capsize=6, elinewidth=2.2)
        label = f"{estimate:+{fmt}}  [{low:+{fmt}}, {high:+{fmt}}]"
        ax.text(.5, .80, label, transform=ax.transAxes, ha="center", fontsize=11, color=INK)
        ax.set_xlim(*limits)
        ax.set_ylim(-.8, .9)
        ax.set_yticks([])
        ax.set_xlabel(unit)
        ax.spines["left"].set_visible(False)
        ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    fig.text(.5, .045, "n = 300 paired tasks; 10,000 resamples stratified by task type. Intervals are taken from the supplied analysis.",
             ha="center", color=MUTED, fontsize=9)
    fig.text(.5, .013, "Intervals crossing zero do not establish a direction. Equal observed success is not proof of equivalence.",
             ha="center", color=MUTED, fontsize=9)
    save(fig, "paired_uncertainty")


def outcomes(paired):
    cells = paired["discordance_table"]
    values = [[cells["both_success"], cells["A_only_success"]],
              [cells["C_only_success"], cells["both_failure"]]]
    labels = [["Both succeeded", "Only A succeeded"], ["Only C succeeded", "Both failed"]]
    fig, ax = plt.subplots(figsize=(7.3, 5.7))
    fig.subplots_adjust(left=.20, right=.94, bottom=.19, top=.78)
    fig.suptitle("Same success count, different task outcomes", y=.97, fontsize=16, fontweight="bold")
    fig.text(.5, .91, "300 paired tasks | A-only successes: 5 | C-only successes: 5", ha="center", color=MUTED, fontsize=10)
    ax.imshow(values, cmap="Blues", vmin=0, vmax=300, aspect="auto")
    for i in range(2):
        for j in range(2):
            v = values[i][j]
            color = "white" if v > 150 else INK
            ax.text(j, i-.17, str(v), ha="center", va="center", fontsize=29, fontweight="bold", color=color)
            ax.text(j, i+.13, labels[i][j], ha="center", va="center", fontsize=10, color=color)
            ax.text(j, i+.32, f"{100*v/300:.2f}% of tasks", ha="center", va="center", fontsize=9, color=color)
    ax.set_xticks([0, 1], ["C succeeded", "C failed"])
    ax.set_yticks([0, 1], ["A succeeded", "A failed"])
    ax.tick_params(length=0, pad=10)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([.5], minor=True)
    ax.set_yticks([.5], minor=True)
    ax.grid(which="minor", color="white", linewidth=5)
    ax.tick_params(which="minor", length=0)
    fig.text(.5, .04, "Exact two-sided McNemar p = 1.0; this does not establish equivalence.", ha="center", color=MUTED, fontsize=9)
    save(fig, "paired_outcomes")


def main():
    summary, paired = load_data()
    style()
    overview(summary)
    task_types(paired)
    uncertainty(paired)
    outcomes(paired)
    print("Generated four figures in SVG and PNG from the published aggregate reports.")


if __name__ == "__main__":
    main()
