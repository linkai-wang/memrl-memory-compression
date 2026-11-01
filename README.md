# MemRL Memory Compression

[����˵��](README_zh.md)

An undergraduate CS project exploring a simple question: **can an agent keep fewer memories and still solve ALFWorld tasks well?**

The current experiment reduces a bank of **300 memories to 195**, a **35% reduction in memory records**. We then compare the full bank and the smaller bank on the same tasks.

**Current status:** the smaller bank loads correctly in MemRL, offline checks passed, and a small pilot completed. The full comparison is underway in the user's Ubuntu environment; final results have not yet been collected in this repository. This page does not claim that compression improves or preserves success rate.

## What changed

We selected existing memories using their content and task coverage, with help from an AI assistant. The 195 retained records keep their original text, Q values, and feedback counts. We did not write new merged summaries or use Q values to choose the subset.

Of the 105 removed records, 11 have reviewed content representatives that remain in the bank. The other 94 were removed to meet the size budget and may contain useful information. Even the reviewed cases are not proof of equivalent task performance.

The smaller bank still covers all 187 recorded task/object/destination combinations and keeps all 151 original retrieval index keys and vectors. **35% fewer records does not mean 35% fewer vectors, tokens, or API costs.**

## The comparison

| Setting | A: full bank | C: smaller bank |
|---|---:|---:|
| Memory records | 300 | 195 |
| Retrieval | MemRL: similarity + Q | MemRL: similarity + Q |
| New tasks | Same 300 | Same 300 |
| Memory and Q updates during testing | Frozen | Frozen |

The 300 tasks come from unused task instances in the **official ALFWorld training pool**, with 50 tasks from each of six task types. They are held out from the earlier runs checked by the selection script. They are **not the official `valid_unseen` split**. Each task runs once per group, giving 600 episodes in total.

We will compare success rate, action decisions, and token usage, and inspect tasks where the two groups disagree. Both groups use the same model, prompts, and MemRL settings. See [the experiment details](docs/experiment.md).

## What is ready

- The 195-record bank passed native loading and cached retrieval checks in Ubuntu.
- The original records, checkpoints, and Q values were preserved.
- The A/C setup passed offline checks and a three-task-per-group pilot.
- Full 300-task-per-group results are pending; pilot outcomes are not presented as final performance.

## Next

Finish the fixed A/C comparison, add complete results and simple charts, and review the tasks on which the groups differ. Later work may turn the selection process into a repeatable periodic memory update. The current experiment tests one fixed subset, not an automatic online consolidation system.

See [the next steps](docs/next_steps.md) and [the result status](results/status.json).

## Repository contents

- `data/`: compression counts, selected IDs, and one decision row per original memory. Full memory texts and vectors are not included.
- `docs/`: experiment design and next steps.
- `results/`: current reporting status; complete evaluation results will be added later.
- `tools/export_results.py`: a small Python tool that checks complete local result summaries and exports aggregate results for publication.

This is a project record with a reporting tool. It is not a standalone installation of MemRL or the full local evaluation runner. The exact frozen task manifest and runnable experiment package are not included in this initial upload, so the published files alone cannot reproduce the full run.

The reporting tool uses only the Python standard library. Its usage is in [tools/README.md](tools/README.md).

## Acknowledgments

This project builds on [MemRL](https://github.com/MemTensor/MemRL) and [ALFWorld](https://github.com/alfworld/alfworld). AI assistance was used for code, memory screening, and documentation. The user runs the experiments in Ubuntu. The selection is not an independent human annotation study.
