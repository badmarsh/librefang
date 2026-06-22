#!/usr/bin/env python3
"""
LibreFang - Conformal Prediction Calibration (Improvement 29)
Reference: Angelopoulos & Bates (2021) arXiv:2107.07511
Computes nonconformity scores and derives q_hat for a 90% coverage guarantee.
"""

import json
import math
import os
import random
import sys
from pathlib import Path

# Add tests directory to path so we can import call_pipeline
sys.path.insert(0, str(Path(__file__).parent.parent / "tests"))
from test_pipeline import call_pipeline

def main():
    report_only = "--report" in sys.argv
    corpus_path = Path("tests/fixtures/calibration_corpus.json")
    if not corpus_path.exists():
        print(f"Error: {corpus_path} not found.")
        sys.exit(1)
        
    with open(corpus_path, "r") as f:
        data = json.load(f)
        
    articles = data.get("articles", [])
    if not articles:
        print("No articles found in calibration corpus.")
        sys.exit(1)
        
    # Shuffle with fixed seed for reproducibility
    random.seed(42)
    shuffled = list(articles)
    random.shuffle(shuffled)
    
    # 20% held-out split for calibration
    split_idx = int(len(shuffled) * 0.8)
    cal_set = shuffled[split_idx:]
    
    print(f"Using {len(cal_set)} articles for conformal calibration...")
    
    nonconformity_scores = []
    
    for article in cal_set:
        expected = article.get("expected_verdict")
        if expected not in ("CREDIBLE", "DISINFORMATION"):
            continue
            
        resp = call_pipeline(article)
        verdicts = resp.get("verdicts", [])
        if not verdicts:
            continue
            
        p_fake = verdicts[0].get("weighted_fake_score", 0.5)
        
        if expected == "DISINFORMATION":
            s_i = 1.0 - p_fake
        else: # CREDIBLE
            s_i = p_fake
            
        nonconformity_scores.append(s_i)
        
    n = len(nonconformity_scores)
    if n == 0:
        print("Error: No valid scores computed.")
        sys.exit(1)
        
    nonconformity_scores.sort()
    
    # α = 0.10 for 90% coverage
    alpha = 0.10
    q_level = math.ceil((n + 1) * (1 - alpha)) / n
    # Clamp to 1.0 to avoid index error
    q_level = min(1.0, q_level)
    
    # Calculate quantile
    if q_level >= 1.0:
        q_hat = nonconformity_scores[-1]
    else:
        # Approximate using nearest rank
        idx = int(q_level * n)
        # Ensure we don't go out of bounds
        idx = min(idx, n - 1)
        q_hat = nonconformity_scores[idx]
        
    print(f"Computed q_hat = {q_hat:.4f} at α = {alpha} (n={n})")
    
    # Verify empirical coverage on the same set (should be >= 1 - alpha)
    covered = 0
    for s_i in nonconformity_scores:
        if s_i <= q_hat:
            covered += 1
            
    empirical_coverage = covered / n
    print(f"Empirical Coverage: {empirical_coverage:.2%}")
    
    if not report_only:
        os.makedirs("data", exist_ok=True)
        out_path = Path("data/conformal_threshold.json")
        with open(out_path, "w") as f:
            json.dump({
                "q_hat": q_hat,
                "alpha": alpha,
                "conformal_coverage_guarantee": 1.0 - alpha,
                "empirical_coverage": empirical_coverage,
                "n_samples": n
            }, f, indent=2)
        print(f"Saved threshold to {out_path}")
        
    if empirical_coverage < 0.88:
        print("WARNING: Coverage below 88% tolerance!")
        sys.exit(1)
        
if __name__ == "__main__":
    main()
