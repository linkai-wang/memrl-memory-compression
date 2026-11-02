# Periodic Memory Compression for MemRL

[中文说明](README_zh.md)

An undergraduate research project exploring **periodic memory compression to improve MemRL**: reducing accumulated memories at stage boundaries while preserving useful experience.

## Current experiment

AI-assisted selection reduced **300 memories to 195 (35% fewer records)**. Retained text and Q values are unchanged; some useful information may be lost.

| Group | Memories | Success |
|---|---:|---:|
| A | 300 | 286/300 (95.33%) |
| C | 195 | 286/300 (95.33%) |

Both used MemRL's similarity + Q retrieval with frozen memory and Q on the same 300 ALFWorld train-pool holdout tasks, not official `valid_unseen`.

**Results:** the success-rate difference was 0 percentage points (95% paired bootstrap interval: −2 to +2). Mean decisions rose 4.66% and solver tokens rose 6.21%; their difference intervals included zero. Repeated-stage compression remains untested.

## Next

Inspect the 10 tasks with different outcomes, then develop reproducible compression and test it across multiple stages within MemRL.

## Details

[Experiment](docs/experiment.md) · [Results](docs/results.md) · [Plan](docs/next_steps.md) · [Data](data/) · [Reporting tool](tools/README.md)

The full local runner is not included. AI assisted code, screening, and documentation.

Built on [MemRL](https://github.com/MemTensor/MemRL); evaluated using [ALFWorld](https://github.com/alfworld/alfworld).
