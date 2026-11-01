"""Export complete AC300 aggregate results. Standard library only; no API calls."""
import argparse
import json
import math
from pathlib import Path

PLAN_SHA256 = "8ddeb8047891e615c87c587e586acdd93725ca6cdfce15023a0ca02d802a3979"
ARMS = {"A_full300": 300, "C_content195": 195}
CELLS = ("both_success", "both_failure", "A_only_success", "C_only_success")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def count(value, name, maximum=300):
    require(type(value) is int and 0 <= value <= maximum, "Invalid count: " + name)
    return value


def number(value, name):
    require(type(value) in (int, float) and math.isfinite(value), "Invalid number: " + name)
    return value


def export(summary, paired):
    require(summary["protocol"] == "alfworld_ac300_frozen_full300_vs_content195_v1", "Different protocol")
    require(summary["plan_canonical_sha256"] == PLAN_SHA256, "Different frozen plan")
    require(summary["complete"] is True and paired["complete"] is True, "Run is incomplete")
    require(summary["planned_tasks_per_arm"] == paired["paired_tasks"] == 300, "Expected 300 paired tasks")
    require(summary["memory_and_q_frozen"] is True, "Memory/Q must be frozen")
    require(paired["status"] == "complete_paired_analysis", "Paired analysis is incomplete")
    require(paired["bank_counts"] == ARMS, "Different memory banks")
    cells = {key: count(paired["discordance_table"][key], key) for key in CELLS}
    require(sum(cells.values()) == 300, "Paired counts do not sum to 300")
    require(summary["paired"]["completed_pairs"] == 300, "Missing completed pairs")
    require(all(summary["paired"][key] == cells[key] for key in CELLS), "Paired tables disagree")
    arms = {}
    for arm, memories in ARMS.items():
        row = summary["arms"][arm]
        require(row["completed"] == 300 and row["pending"] == 0, "Incomplete arm: " + arm)
        require(row["memory_count"] == memories, "Unexpected bank size")
        successes = count(row["successes"], arm)
        only = "A_only_success" if arm == "A_full300" else "C_only_success"
        require(successes == cells["both_success"] + cells[only], "Success count disagrees with paired table")
        require(math.isclose(number(row["success_rate"], "SR"), successes / 300, abs_tol=1e-9), "SR disagrees with count")
        decisions = number(row["mean_decisions"], "mean_decisions")
        require(0 <= decisions <= 50, "Decision mean out of range")
        tokens = {key: count(row["solver_usage"][key], key, maximum=10**15)
                  for key in ("prompt_tokens", "completion_tokens", "total_tokens")}
        require(tokens["total_tokens"] == tokens["prompt_tokens"] + tokens["completion_tokens"], "Token totals disagree")
        arms[arm] = {"memory_count": memories, "completed": 300, "successes": successes,
                     "success_rate": successes / 300, "mean_decisions": decisions, "solver_tokens": tokens}
    sr = paired["all_task_paired_differences"]["success_difference_percentage_points"]
    difference = 100 * (arms["C_content195"]["successes"] - arms["A_full300"]["successes"]) / 300
    require(sr["n"] == 300 and math.isclose(number(sr["C_minus_A"], "SR difference"), difference, abs_tol=1e-9), "SR contrast disagrees")
    ci = sr["ci95"]
    require(isinstance(ci, list) and len(ci) == 2, "Missing 95% interval")
    low, high = (number(value, "CI endpoint") for value in ci)
    require(-100 <= low <= high <= 100, "Invalid SR interval")
    p = number(paired["exact_mcnemar_two_sided_p"], "p value")
    require(0 <= p <= 1, "Invalid p value")
    return {"status": "complete_aggregate_results", "plan_canonical_sha256": PLAN_SHA256,
            "paired_tasks": 300, "episodes": 600, "record_reduction_fraction": 0.35,
            "task_set_role": "unused_task_instances_from_official_train_pool_not_valid_unseen",
            "arms": arms, "paired_outcomes": cells,
            "success_difference_percentage_points_C_minus_A": {"estimate": difference, "ci95": [low, high]},
            "exact_mcnemar_two_sided_p": p, "memory_and_q_frozen": True,
            "formal_noninferiority_test_performed": False,
            "verification_scope": "summary_consistency_only_not_episode_log_audit"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--paired", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = export(json.loads(args.summary.read_text(encoding="utf-8-sig")),
                        json.loads(args.paired.read_text(encoding="utf-8-sig")))
        # Never overwrite an input or any other file, including an earlier report.
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(1, f"Export refused: {error}\n")
    print("Complete aggregate results exported.")


if __name__ == "__main__":
    main()
