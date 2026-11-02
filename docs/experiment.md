# Current validation experiment for MemRL memory compression

The completed aggregate results and paired analysis were received on 2026-11-02. See [results and interpretation](results.md). The settings below describe the fixed protocol used for that run.

## Place in the research

The overall topic is periodic memory compression as a possible improvement to MemRL's memory management. The intended system compresses accumulated memories at stage boundaries and then continues to collect and use experience. ALFWorld supplies the agent tasks for this first evaluation; the research target is MemRL's memory mechanism.

The current experiment checks one fixed compression step. A favorable result would motivate further experiments, but would not establish the benefit of repeated compression or performance on other benchmarks.

## Question

How does keeping 195 of 300 existing memories affect MemRL's task success and resource use when retrieval stays the same? We measure this using ALFWorld as the current benchmark.

This experiment studies the effect of one fixed memory selection. It does not isolate every selection rule, compare against random pruning, or test periodic updates during training.

## Building the smaller bank

The selection considered memory content and structured coverage: task type, object, any extra condition, and destination. An AI assistant reviewed the candidates. Q values were not a selection score. Retained records are unchanged copies, including their own Q values and feedback counts.

| Item | Before | After |
|---|---:|---:|
| Memory records | 300 | 195 |
| Task/object/destination combinations | 187 | 187 |
| Combinations with a successful example | 181 | 181 |
| Retrieval index keys and cached vectors | 151 | 151 |
| Failure records | 16 | 14 |

Matching these counts does not guarantee that every useful strategy was preserved. Of the 105 removals, 11 have reviewed surviving representatives and 94 are capacity removals with possible information loss. Two failure records about heating a mug and placing it at a coffee machine were removed from the active bank; the original bank remains intact. There are 53 retained records whose source goal differs from the retrieval index text. These inherited mappings were preserved rather than silently changed for this test.

The public [decision table](../data/retention_decisions.csv) records which memories were retained. `coverage_anchor_id` means that another record covers the structured task condition; it does not establish equivalent strategy content. Full strategy texts are not included, so the metadata alone cannot independently verify semantic equivalence.

## Tasks and paired execution

We selected 300 new task instances from the installed official ALFWorld `train` pool, excluding earlier known training, development, and evaluation tasks. The selection checks task IDs, source task IDs, game-file hashes, and canonical problem hashes. Zero overlap under these checks means separate task instances, not completely unseen objects or task patterns.

Each of these six types has 50 tasks:

- `look_at_obj_in_light`
- `pick_and_place_simple`
- `pick_clean_then_place_in_recep`
- `pick_cool_then_place_in_recep`
- `pick_heat_then_place_in_recep`
- `pick_two_obj_and_place`

Both groups attempt every task once. A runs first on 150 tasks and C runs first on 150 tasks. Task selection uses seed 20261101; arm order uses seed 20261102. Local seeds do not make a remote model's outputs fully deterministic.

## Shared settings

| Setting | Value in both groups |
|---|---|
| Solver | `deepseek-flash` |
| Temperature | 0.6 |
| Thinking | Disabled |
| Output token limit per decision | 4096 |
| Decision limit per task | 50 |
| Embedding model | `BAAI/bge-m3`, 1024 dimensions |
| Index candidates | 5 |
| Retrieved memories | Up to 3 |
| Similarity threshold | 0.62 |
| Similarity / Q weights | 0.5 / 0.5 |
| Epsilon / recency boost | 0 / 0 |
| Memory and Q updates | Disabled during evaluation |
| Static few-shot examples | None |

The prompts and legal action menu policy are also shared. The local preflight reported the frozen plan fingerprint `8ddeb8047891e615c87c587e586acdd93725ca6cdfce15023a0ca02d802a3979`.

## Checks and reporting

User-provided Ubuntu outputs confirm native loading of both banks, original Q and content consistency, cached retrieval checks, an environment reset/step check, and a completed three-task-per-group pilot. These are engineering checks, not evidence about the final 300-task success rate. Cached-vector replay does not validate new query embeddings.

Success is taken from the environment's `won` flag. After all 600 episodes are committed, report successes out of 300 per group, the paired success-rate difference with uncertainty, decisions, and solver token usage. Also report decisions and tokens on tasks both groups solved, so failures that stop early do not misleadingly look efficient. Include the counts of A-only and C-only successes.

There is one model run per task and group. Similar observed success rates would not by themselves prove equivalence or noninferiority. The current train-pool holdout does not establish official `valid_unseen` performance.
