# Periodic Memory Compression for MemRL

[中文说明](README_zh.md)

An undergraduate research project exploring **periodic memory compression to improve MemRL**: reducing accumulated memories at stage boundaries while preserving useful experience.

## Current experiment

AI-assisted selection reduced **300 memories to 195 (35% fewer records)**. Retained text and Q values are unchanged; some useful information may be lost.

| Group | Memory bank |
|---|---|
| A | Original 300 |
| C | Selected 195 |

Both use MemRL's similarity + Q retrieval with frozen memory and Q. They attempt the same 300 held-out tasks from the ALFWorld training pool—a custom holdout, not official `valid_unseen`.

Loading, offline checks, and a small pilot passed. **Full results are pending.** Repeated compression across training stages remains to be tested.

## Next

Compare success rate, decisions, and tokens, then develop and test repeated stage-based compression within MemRL.

## Details

[Experiment](docs/experiment.md) · [Plan](docs/next_steps.md) · [Data](data/) · [Results](results/status.json) · [Reporting tool](tools/README.md)

The full local runner is not included. AI assisted code, screening, and documentation.

Built on [MemRL](https://github.com/MemTensor/MemRL); evaluated using [ALFWorld](https://github.com/alfworld/alfworld).
