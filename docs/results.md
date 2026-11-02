# First compression-step results

The current MemRL experiment compares the original 300-memory bank (A) with the selected 195-memory bank (C). Both use the same similarity + Q retrieval, frozen memory and Q, and the same 300 held-out ALFWorld train-pool task instances. These are custom holdout tasks, not official `valid_unseen`.

## Main results

| Measure | A: 300 memories | C: 195 memories |
|---|---:|---:|
| Completed tasks | 300 | 300 |
| Successes | 286 (95.33%) | 286 (95.33%) |
| Mean decisions per task | 13.87 | 14.52 |
| Total solver tokens | 20,643,077 | 21,925,321 |
| Mean presented memory context, characters | 3285.22 | 3337.25 |
| Invalid actions | 107 | 86 |

C uses 35% fewer memory records. Its observed mean decision count is 4.66% higher and solver token use is 6.21% higher. The uncertainty intervals below do not establish a consistent increase in either measure.

## Paired differences

All differences are C minus A. Intervals are 95% paired bootstrap intervals, with 10,000 resamples within task type.

| Measure | Observed difference | 95% interval |
|---|---:|---:|
| Success rate, percentage points | 0.00 | −2.00 to +2.00 |
| Decisions per task | +0.647 | −0.377 to +1.687 |
| Solver tokens per task | +4274 | −5855 to +14225 |
| Presented memory characters per task | +52.03 | +30.90 to +73.48 |

Both groups solved 281 tasks and failed 9 tasks; A alone solved 5 and C alone solved 5. The exact two-sided McNemar p-value is 1.0. This gives no evidence of a success-rate difference in this run; it is not proof of equivalence or a probability that the banks are equivalent.

On the 281 tasks both groups solved, C used an observed 0.605 more decisions per task (interval −0.317 to +1.555) and 3571 more solver tokens (−4569 to +11854). Those intervals also include zero. The higher observed resource use is therefore not limited to tasks where success differs, but its direction remains uncertain.

## Task types

Each task type has 50 paired tasks. These are descriptive subgroup counts.

| Task type | A successes | C successes |
|---|---:|---:|
| Clean then place | 47 | 47 |
| Look at object in light | 50 | 50 |
| Cool then place | 42 | 41 |
| Simple pick and place | 50 | 50 |
| Place two objects | 50 | 50 |
| Heat then place | 47 | 48 |

Cooling has the lowest success count in both groups. The one-task shifts in cooling and heating do not establish a task-specific compression effect.

## Interpretation

This first test achieved a smaller active memory bank with the same observed overall success rate. It has not demonstrated lower inference token use or fewer decisions. The memory context presented to the solver was slightly longer in C, despite fewer records being stored.

The success-rate interval still includes differences in either direction. No formal noninferiority test was performed. There is one remote model run per task and group, and local seeds do not eliminate remote sampling variation. This fixed-bank comparison does not establish the benefit of repeated compression during continued MemRL training.

Next, inspect the 10 tasks with different outcomes and their retrieval traces. Keep the current test fixed; use separate development data for subsequent method changes.

## Evidence

The user ran the evaluation and paired-analysis script in Ubuntu and supplied the aggregate reports on 2026-11-02. The assistant checked their mutual consistency, per-type totals, and reported means. It did not independently read the underlying 600 episode logs or recompute the bootstrap samples from those logs.

Machine-readable files: [summary](../results/summary.json), [paired analysis](../results/paired_analysis.json), and [status](../results/status.json). Full local episode traces are not included in this repository.
