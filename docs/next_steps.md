# Next steps toward periodic memory compression in MemRL

The research goal is to improve MemRL's memory management through compression at stage boundaries. ALFWorld is the current benchmark for checking the method. The present A/C experiment is a first check of one compression step within this larger plan.

1. Finish the frozen A/C run: 300 tasks for each group, using the existing resume mechanism. Keep the selected memories, tasks, model, prompts, and Q values fixed.
2. Check that all 600 episodes are present, then run the existing local paired-analysis script. Keep partial results clearly separate until the run is complete.
3. Update this repository with complete aggregate results: successes, success-rate difference and uncertainty, decisions, and token usage. Add two or three readable charts.
4. Inspect tasks where only one group succeeds. Look for missing strategies, retrieval differences, and model variation; do not assume each difference was caused by a particular removed memory.
5. Write a short conclusion that reflects the data, including an unfavorable or uncertain result if that is what we find.
6. Make the compression step reproducible within MemRL. Use a separate development set to choose when compression happens, how much memory to retain, and how to protect useful experience. Compare against random or simpler selection baselines.
7. Test multiple stages of experience accumulation and compression, comparing against MemRL without compression. Track task success, memory growth, and measured resource use after each stage. Keep the current fixed-bank experiment distinct from this later repeated-stage experiment.
8. If the method is supported by the results, consider another agent-task benchmark to check how broadly it applies. This is future work; no cross-benchmark benefit is claimed now.

The current 300 evaluation tasks must not become the tuning set for a revised memory bank that is then presented as a fresh test on those same tasks. The original 300-record bank stays available for comparison and recovery.

The initial upload documents the method and selection metadata. A later reproducibility update can include the frozen task manifest and a portable runner after reviewing local paths, dependencies, and what data can be shared.
