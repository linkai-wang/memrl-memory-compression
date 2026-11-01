# Updating the public results

`export_results.py` only reads two existing local summary files and writes an aggregate report. It does not run ALFWorld, call a model, change the experiment, or upload to GitHub.

After the full evaluation and its existing paired analysis have finished:

```bash
python tools/export_results.py \
  --summary /path/to/eval_summary.json \
  --paired /path/to/paired_analysis.json \
  --out results/summary.json
```

The tool refuses incomplete runs, inconsistent paired counts, and a different experiment fingerprint. Only selected aggregate fields are exported. Original API logs, credentials, paths, memory texts, and individual episode traces are not copied. This is a consistency check of the summaries, not an independent audit of the 600 episode logs.

Review the generated report before committing it. Then update the README and `results/status.json` to reflect the completed run; the script does not change them automatically.

Run the reporting-tool tests locally with:

```bash
python -m unittest discover -s tests -v
```
