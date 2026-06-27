# LibreFang — calibrate_weights.py
# Part of fix: Fix 4 — Add ensemble weight validation on Slovak data + calibration stub
# Author: librefang
# Date: 2026-06-27

import argparse
import json
import numpy as np
import pandas as pd
from sklearn.metrics import fbeta_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
import tomlkit

def generate_weight_combinations(step=0.02, sum_target=1.0, keys=['ml', 'trip', 'wiki', 'coh', 'src']):
    """Generate combinations of weights that sum to sum_target with a given step size."""
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
    y_true = df['ground_truth']
    y_pred_prob = df['agent_scores'].apply(
        lambda scores: sum(scores.get(k, 0) * weights.get(k, 0) for k in weights)
    )
    y_pred = (y_pred_prob >= 0.5).astype(int)
    return fbeta_score(y_true, y_pred, beta=2.0, zero_division=0)

def calibrate_probabilities(df, best_weights, target_fpr=0.05):
    """
    Applies Platt Scaling (Logistic Regression) to the weighted ensemble scores
    to map them to true probabilities, ensuring the FPR is strictly bounded.
    """
    print(f"Applying Platt scaling to bound FPR to {target_fpr:.1%}...")
    
    y_true = df['ground_truth'].values
    
    # Calculate the raw weighted ensemble score for each sample
    X_raw = df['agent_scores'].apply(
        lambda scores: sum(scores.get(k, 0) * best_weights.get(k, 0) for k in best_weights)
    ).values.reshape(-1, 1)

    # Fit Logistic Regression on raw scores
    # We use penalty=None to avoid shrinking parameters, we just want simple 1D calibration
    lr = LogisticRegression(penalty=None, solver='lbfgs')
    lr.fit(X_raw, y_true)
    
    # Platt scaling equation: P(y=1|x) = 1 / (1 + exp(-(A*x + B)))
    A = lr.coef_[0][0]
    B = lr.intercept_[0]
    print(f"Calibration Parameters -> A: {A:.4f}, B: {B:.4f}")
    
    # Predict calibrated probabilities
    calibrated_probs = lr.predict_proba(X_raw)[:, 1]
    
    # Find decision threshold that satisfies FPR <= 0.05
    thresholds = np.sort(np.unique(calibrated_probs))
    best_threshold = 0.5
    
    for t in thresholds:
        y_pred = (calibrated_probs >= t).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        fpr = fp / (fp + tn)
        if fpr <= target_fpr:
            best_threshold = t
            break
            
    print(f"Calibrated Threshold for FPR<={target_fpr}: {best_threshold:.4f}")
    return A, B, best_threshold

def main():
    parser = argparse.ArgumentParser(description="Calibrate LibreFang ensemble weights for Slovak data.")
    parser.add_argument("--verdicts", required=True, help="Path to JSONL file of confirmed verdicts")
    parser.add_argument("--apply", action="store_true", help="Apply best weights and calibration parameters to config.toml")
    args = parser.parse_args()

    df = load_verdicts(args.verdicts)
    if df.empty:
        print("No verdicts found.")
        return

    print("Generating weight combinations...")
    # Step = 0.05 for reasonable execution time during tests
    combinations = list(generate_weight_combinations(step=0.05))
    
    print(f"Evaluating {len(combinations)} combinations...")
    results = []
    for weights in combinations:
        f2 = evaluate_weights(df, weights)
        results.append({"weights": weights, "f2": f2})

    results.sort(key=lambda x: x['f2'], reverse=True)
    best_weights = results[0]['weights']
    
    print("\nTop 5 weight combinations:")
    for i in range(min(5, len(results))):
        res = results[i]
        print(f"  {i+1}. F2-score: {res['f2']:.4f} | Weights: {res['weights']}")

    # IMPROVE-1 Calibration Step
    print("\n--- Running Calibration Corpus Methodology ---")
    A, B, threshold = calibrate_probabilities(df, best_weights, target_fpr=0.05)

    if args.apply:
        config_path = "config.toml"
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config_doc = tomlkit.load(f)
            
            if "disinfo_pipeline" in config_doc:
                if "baseline_weights" not in config_doc["disinfo_pipeline"]:
                    config_doc["disinfo_pipeline"]["baseline_weights"] = tomlkit.table()
                
                target_table = config_doc["disinfo_pipeline"]["baseline_weights"]
                for k, v in best_weights.items():
                    target_table[k] = v
                    
                if "calibration" not in config_doc["disinfo_pipeline"]:
                    config_doc["disinfo_pipeline"]["calibration"] = tomlkit.table()
                    
                calib_table = config_doc["disinfo_pipeline"]["calibration"]
                calib_table["platt_A"] = A
                calib_table["platt_B"] = B
                calib_table["threshold_fpr5"] = threshold
                
                with open(config_path, "w", encoding="utf-8") as f:
                    tomlkit.dump(config_doc, f)
                print(f"\nSuccessfully applied best weights and calibration parameters to {config_path}.")
            else:
                print("\nError: [disinfo_pipeline] section not found in config.toml.")
        except Exception as e:
            print(f"\nFailed to apply weights: {e}")

if __name__ == "__main__":
    main()
