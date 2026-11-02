# Next steps toward periodic memory compression in MemRL

The research goal is to improve MemRL's memory management through compression at stage boundaries. ALFWorld is the current benchmark for checking the method. The first fixed-bank A/C experiment and paired analysis are complete: both groups solved 286/300 tasks, with no demonstrated efficiency gain. See [results](results.md).

1. Inspect the 10 tasks where only one group succeeds. Compare retrieved memories and action traces, considering model variation as well as missing strategies. Do not assume each difference was caused by a removed memory.
2. Examine context length and resource-use differences across tasks, including the 281 tasks both groups solved. Fewer stored records did not shorten the presented memory context in this run.
3. Make the compression step reproducible within MemRL. Use a separate development set to choose when compression happens, how much memory to retain, and how to protect useful experience. Compare against random or simpler selection baselines.
4. Test multiple stages of experience accumulation and compression against MemRL without compression. Track task success, memory growth, and measured resource use after each stage. The first fixed-bank experiment does not establish these repeated-stage effects.
5. Consider another agent-task benchmark if later evidence supports the method. No cross-benchmark benefit is claimed now.

The current 300 evaluation tasks must not become the tuning set for a revised memory bank that is then presented as a fresh test on those same tasks. The original 300-record bank stays available for comparison and recovery.

The initial upload documents the method and selection metadata. A later reproducibility update can include the frozen task manifest and a portable runner after reviewing local paths, dependencies, and what data can be shared.
