"""Synthetic fixtures test the exporter, not research performance."""
import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("export_results", Path(__file__).resolve().parents[1] / "tools/export_results.py")
reporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reporter)


def fixture():
    cells = {"both_success": 240, "both_failure": 30, "A_only_success": 20, "C_only_success": 10}
    arms = {name: {"completed": 300, "pending": 0, "memory_count": size,
                   "successes": successes, "success_rate": successes / 300,
                   "mean_decisions": 12.5, "solver_usage": {"prompt_tokens": 1000, "completion_tokens": 200, "total_tokens": 1200}}
            for name, size, successes in (("A_full300", 300, 260), ("C_content195", 195, 250))}
    summary = {"protocol": "alfworld_ac300_frozen_full300_vs_content195_v1",
               "plan_canonical_sha256": reporter.PLAN_SHA256, "complete": True,
               "planned_tasks_per_arm": 300, "memory_and_q_frozen": True,
               "arms": arms, "paired": {"completed_pairs": 300, **cells},
               "private_path": "DO_NOT_PUBLISH", "api_key": "DO_NOT_PUBLISH"}
    paired = {"status": "complete_paired_analysis", "complete": True, "paired_tasks": 300,
              "bank_counts": reporter.ARMS, "discordance_table": cells,
              "all_task_paired_differences": {"success_difference_percentage_points":
                  {"n": 300, "C_minus_A": -100 / 30, "ci95": [-7, 0]}},
              "exact_mcnemar_two_sided_p": 0.1}
    return summary, paired


class ExportTests(unittest.TestCase):
    def test_complete_export_and_sensitive_extras_excluded(self):
        summary, paired = fixture()
        result = reporter.export(summary, paired)
        self.assertEqual(result["episodes"], 600)
        self.assertEqual(result["arms"]["C_content195"]["successes"], 250)
        self.assertNotIn("DO_NOT_PUBLISH", str(result))

    def test_incomplete_refused(self):
        summary, paired = fixture()
        summary["complete"] = False
        with self.assertRaises(ValueError):
            reporter.export(summary, paired)

    def test_inconsistent_success_count_refused(self):
        summary, paired = fixture()
        summary["arms"]["C_content195"]["successes"] = 249
        with self.assertRaises(ValueError):
            reporter.export(summary, paired)

    def test_changed_plan_refused(self):
        summary, paired = fixture()
        summary["plan_canonical_sha256"] = "different"
        with self.assertRaises(ValueError):
            reporter.export(summary, paired)

    def test_invalid_interval_refused(self):
        summary, paired = fixture()
        paired = copy.deepcopy(paired)
        paired["all_task_paired_differences"]["success_difference_percentage_points"]["ci95"] = [float("nan"), 0]
        with self.assertRaises(ValueError):
            reporter.export(summary, paired)


if __name__ == "__main__":
    unittest.main()
