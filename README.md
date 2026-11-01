# Periodic Memory Compression for MemRL

[中文说明](README_zh.md)

An undergraduate CS project exploring **periodic memory compression to improve MemRL's memory management**. The goal is to compress accumulated memories at stage boundaries while preserving useful experience for later tasks. ALFWorld is the agent-task benchmark used for the current evaluation.

## Current progress

We reduced a bank of **300 memories to 195 — 35% fewer records** through AI-assisted content and task-coverage selection. Retained records keep their original text, Q values, and feedback counts. The selection includes capacity tradeoffs and may lose information.

Native loading, offline retrieval checks, and a small pilot have passed. **Full evaluation results are pending.** Repeated compression across training stages has not yet been evaluated.

## A/C comparison

| Group | Memories | Retrieval |
|---|---:|---|
| A | Original 300 | MemRL: similarity + Q |
| C | Selected 195 | MemRL: similarity + Q |

Both groups attempt the same 300 held-out task instances from the ALFWorld training pool, with memory and Q frozen. This is a custom holdout, not the official `valid_unseen` split. We will compare success rate, decisions, and token usage.

## Next steps

Finish the comparison, publish complete results, and inspect differences. Then develop a repeatable compression step within MemRL and test it across multiple stages of experience accumulation.

## Details

- [Experiment and limitations](docs/experiment.md)
- [Next-step plan](docs/next_steps.md)
- [Compression data](data/) · [Result status](results/status.json)
- [Results export tool](tools/README.md)

This repository contains project notes, selection metadata, and a reporting tool; the full local experiment runner is not included.

Built on [MemRL](https://github.com/MemTensor/MemRL), with [ALFWorld](https://github.com/alfworld/alfworld) for evaluation. AI assisted code, screening, and documentation; experiments are run by the user in Ubuntu.
