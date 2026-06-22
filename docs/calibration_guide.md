# Ensemble Weight Calibration Guide

This guide explains how to validate and recalibrate the LibreFang disinformation-detection ensemble weights for a specific language corpus (e.g., Slovak-language claims). The default weights derive from a general multilingual corpus (arXiv:2508.10143) and may not be optimal for your specific deployment.

## 1. Collect a Labelled Verdict Set
You need at least 50 human-confirmed verdicts to perform a meaningful calibration.
The calibration script expects a JSONL file with the following schema:
```json
{
  "claim_id": "c12345",
  "agent_scores": {
    "ml": 0.85,
    "trip": 0.40,
    "wiki": 0.60,
    "coh": 0.70,
    "src": 0.95
  },
  "ground_truth": 1
}
```
*Note: `ground_truth` should be `1` for confirmed disinformation, and `0` for credible claims.*

## 2. Run Calibration Script
Once you have your `verdicts.jsonl` file, run the grid-search calibration script:
```bash
python scripts/calibrate_weights.py --verdicts path/to/verdicts.jsonl
```
This script evaluates weight combinations (summing to 1) with a step size of 0.02 and optimises for the **F2-score**, penalising false negatives (missed disinformation) more heavily than false positives.

## 3. Interpret the Output and Apply
The script outputs the top 5 weight combinations and their corresponding F2 scores.
Compare the best F2 score against the score of your current weights.
If the new weights offer a substantial improvement without over-fitting, apply them automatically by re-running:
```bash
python scripts/calibrate_weights.py --verdicts path/to/verdicts.jsonl --apply
```
This will cleanly update the `[disinfo_pipeline.baseline_weights]` section in `config.toml`.
