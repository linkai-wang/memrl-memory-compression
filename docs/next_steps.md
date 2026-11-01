# Next steps

1. Finish the frozen A/C run: 300 tasks for each group, using the existing resume mechanism. Keep the selected memories, tasks, model, prompts, and Q values fixed.
2. Check that all 600 episodes are present, then run the existing local paired-analysis script. Keep partial results clearly separate until the run is complete.
3. Update this repository with complete aggregate results: successes, success-rate difference and uncertainty, decisions, and token usage. Add two or three readable charts.
4. Inspect tasks where only one group succeeds. Look for missing strategies, retrieval differences, and model variation; do not assume each difference was caused by a particular removed memory.
5. Write a short conclusion that reflects the data, including an unfavorable or uncertain result if that is what we find.
6. For a later experiment, make selection reproducible and consider random or simpler selection baselines. Then investigate periodic memory updates with a separate development set and new evaluation tasks.

The current 300 evaluation tasks must not become the tuning set for a revised memory bank that is then presented as a fresh test on those same tasks. The original 300-record bank stays available for comparison and recovery.

The initial upload documents the method and selection metadata. A later reproducibility update can include the frozen task manifest and a portable runner after reviewing local paths, dependencies, and what data can be shared.
