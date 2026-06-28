#!/usr/bin/env python3
import json
import argparse
import numpy as np
import scipy.stats

def compute_variance_penalty(timestamps):
    if len(timestamps) < 3:
        return 0.0

    timestamps = np.sort(timestamps)
    delays = np.diff(timestamps)
    
    if len(delays) < 2 or np.std(delays) == 0:
        return 1.0  # Perfect uniformity (zero variance) is highly synthetic

    # Normalize delays to [0, 1] for uniform comparison
    d_min = np.min(delays)
    d_max = np.max(delays)
    
    # If all delays are the same, it's perfectly uniform
    if d_max == d_min:
        return 1.0
        
    normalized_delays = (delays - d_min) / (d_max - d_min)
    
    # Test against uniform distribution on [0, 1]
    # D_unif is the KS statistic (distance). Lower means closer to uniform.
    ks_stat_unif, p_val_unif = scipy.stats.kstest(normalized_delays, 'uniform')
    
    # Fit log-normal to original delays (organic bursty behavior)
    shape, loc, scale = scipy.stats.lognorm.fit(delays[delays > 0])
    ks_stat_lognorm, p_val_lognorm = scipy.stats.kstest(delays, 'lognorm', args=(shape, loc, scale))
    
    # Penalty is 1.0 if it's perfectly uniform (ks_stat_unif == 0)
    # Penalty is 0.0 if it's perfectly log-normal (ks_stat_lognorm == 0 and not uniform)
    # A simple mapping: variance_penalty = 1.0 - ks_stat_unif
    # We can also incorporate lognorm: if it's very lognormal, reduce penalty.
    
    penalty = 1.0 - ks_stat_unif
    
    # Bound the penalty between 0.0 and 1.0
    penalty = max(0.0, min(1.0, penalty))
    
    # If the variance is very small compared to the mean, it's also highly synthetic
    cv = np.std(delays) / np.mean(delays)
    if cv < 0.1:
        penalty = max(penalty, 0.9)
        
    return penalty, ks_stat_unif, ks_stat_lognorm

def main():
    parser = argparse.ArgumentParser(description="Variance Manipulation Penalty (arXiv:2503.03775)")
    parser.add_argument("--actor", type=str, required=True, help="JSON file with timestamps for the actor")
    args = parser.parse_args()

    with open(args.actor, "r") as f:
        timestamps = json.load(f)
        
    if not timestamps or len(timestamps) < 2:
        print(json.dumps({
            "error": "Not enough timestamps",
            "variance_penalty": 0.0
        }))
        return

    penalty, d_unif, d_lognorm = compute_variance_penalty(timestamps)
    
    result = {
        "variance_penalty": float(penalty),
        "ks_stat_uniform": float(d_unif),
        "ks_stat_lognorm": float(d_lognorm)
    }
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
