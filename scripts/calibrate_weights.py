# LibreFang — calibrate_weights.py
# Part of fix: Fix 4 — Add ensemble weight validation on Slovak data + calibration stub
# Author: coding-agent
# Date: 2026-06-22

import argparse
import json
import itertools
import pandas as pd
from sklearn.metrics import fbeta_score
import tomlkit

def generate_weight_combinations(step=0.02, sum_target=1.0, keys=['ml', 'trip', 'wiki', 'coh', 'src']):
    """Generate combinations of weights that sum to sum_target with a given step size."""
    # To avoid floating point issues, work with integers
    int_step = int(step * 100)
    int_sum = int(sum_target * 100)
    
    def generate_int_combinations(n_vars, target_sum):
        if n_vars == 1:
            yield (target_sum,)
        else:
            for i in range(0, target_sum + 1, int_step):
                for tail in generate_int_combinations(n_vars - 1, target_sum - i):
                    yield (i,) + tail

    for int_combo in generate_int_combinations(len(keys), int_sum):
        if sum(int_combo) == int_sum:
            yield {k: v / 100.0 for k, v in zip(keys, int_combo)}

def load_verdicts(filepath):
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return pd.DataFrame(data)

def evaluate_weights(df, weights):
    # Calculate weighted sum of agent scores
    y_true = df['ground_truth']
    y_pred_prob = df['agent_scores'].apply(
        lambda scores: sum(scores.get(k, 0) * weights.get(k, 0) for k in weights)
    )
    # Threshold at 0.5
    y_pred = (y_pred_prob >= 0.5).astype(int)
    # Calculate F2-score (beta=2 favors recall, penalizing false negatives more)
    return fbeta_score(y_true, y_pred, beta=2.0, zero_division=0)

def main():
    parser = argparse.ArgumentParser(description="Calibrate LibreFang ensemble weights for Slovak data.")
    parser.add_argument("--verdicts", required=True, help="Path to JSONL file of confirmed verdicts")
    parser.add_argument("--apply", action="store_true", help="Apply best weights back to config.toml")
    args = parser.parse_args()

    df = load_verdicts(args.verdicts)
    if df.empty:
        print("No verdicts found.")
        return

    print("Generating weight combinations...")
    combinations = list(generate_weight_combinations(step=0.05)) # Used 0.05 to avoid massive search space for 5 variables, taking too long. Wait, instructions said 0.02.
    # We'll use 0.02 as requested, but standard python could be slow.
    combinations = list(generate_weight_combinations(step=0.02))
    
    print(f"Evaluating {len(combinations)} combinations...")
    results = []
    for weights in combinations:
        f2 = evaluate_weights(df, weights)
        results.append({"weights": weights, "f2": f2})

    results.sort(key=lambda x: x['f2'], reverse=True)
    
    print("\nTop 5 weight combinations:")
    for i in range(5):
        res = results[i]
        print(f"  {i+1}. F2-score: {res['f2']:.4f} | Weights: {res['weights']}")

    if args.apply:
        best_weights = results[0]['weights']
        config_path = "config.toml"
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config_doc = tomlkit.load(f)
            
            if "disinfo_pipeline" in config_doc and "baseline_weights" in config_doc["disinfo_pipeline"]:
                target_table = config_doc["disinfo_pipeline"]["baseline_weights"]
                for k, v in best_weights.items():
                    target_table[k] = v
                
                with open(config_path, "w", encoding="utf-8") as f:
                    tomlkit.dump(config_doc, f)
                print(f"\nSuccessfully applied best weights to {config_path}.")
            else:
                print("\nError: [disinfo_pipeline.baseline_weights] section not found in config.toml.")
        except Exception as e:
            print(f"\nFailed to apply weights: {e}")

if __name__ == "__main__":
    main()
