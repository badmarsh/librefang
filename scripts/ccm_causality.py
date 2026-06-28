#!/usr/bin/env python3
import json
import argparse
import numpy as np
import scipy.stats
from scipy.spatial import KDTree

def reconstruct_manifold(ts, E, tau):
    """Reconstructs the shadow manifold using delay coordinates."""
    N = len(ts)
    if N - (E - 1) * tau <= 0:
        return None, None
    
    manifold = []
    valid_indices = []
    for i in range((E - 1) * tau, N):
        point = [ts[i - j * tau] for j in range(E)]
        manifold.append(point)
        valid_indices.append(i)
    return np.array(manifold), np.array(valid_indices)

def ccm_cross_map(X_manifold, X_indices, Y_ts, E):
    """
    Computes cross-map skill from X to Y. 
    X_manifold: delay coordinate vectors of X.
    X_indices: the original time indices corresponding to rows of X_manifold.
    Y_ts: original time series of Y.
    E: embedding dimension.
    """
    if X_manifold is None or len(X_manifold) <= E + 1:
        return 0.0
        
    tree = KDTree(X_manifold)
    # Find E+2 neighbors because the first one might be the point itself (distance 0)
    k = E + 2
    if len(X_manifold) < k:
        k = len(X_manifold)
        
    distances, indices = tree.query(X_manifold, k=k)
    
    Y_pred = []
    Y_true = []
    
    for i in range(len(X_manifold)):
        dists = distances[i]
        idx = indices[i]
        
        # Exclude self
        valid_mask = idx != i
        dists = dists[valid_mask][:E+1]
        idx = idx[valid_mask][:E+1]
        
        if len(dists) == 0:
            continue
            
        # Add a tiny epsilon to prevent division by zero
        min_dist = dists[0]
        if min_dist == 0:
            min_dist = 1e-6
            
        weights = np.exp(-dists / min_dist)
        
        # Avoid all weights being exactly 0 or sum to 0
        weight_sum = np.sum(weights)
        if weight_sum == 0:
            weights = np.ones_like(weights) / len(weights)
        else:
            weights = weights / weight_sum
            
        # Target values are from Y at the same time indices
        neighbor_time_indices = X_indices[idx]
        y_targets = Y_ts[neighbor_time_indices]
        
        y_est = np.sum(weights * y_targets)
        
        Y_pred.append(y_est)
        Y_true.append(Y_ts[X_indices[i]])
        
    Y_pred = np.array(Y_pred)
    Y_true = np.array(Y_true)
    
    # Calculate Pearson correlation coefficient
    if len(Y_pred) < 2 or np.std(Y_pred) == 0 or np.std(Y_true) == 0:
        return 0.0
        
    rho, _ = scipy.stats.pearsonr(Y_pred, Y_true)
    return max(0.0, float(rho))

def bin_timestamps(timestamps, t_min, t_max, bins):
    """Bins timestamps into a histogram."""
    hist, _ = np.histogram(timestamps, bins=bins, range=(t_min, t_max))
    return hist

def main():
    parser = argparse.ArgumentParser(description="CCM Causality Analysis")
    parser.add_argument("--actor1", type=str, required=True, help="JSON file with timestamps for actor 1")
    parser.add_argument("--actor2", type=str, required=True, help="JSON file with timestamps for actor 2")
    parser.add_argument("--E", type=int, default=3, help="Embedding dimension")
    parser.add_argument("--tau", type=int, default=1, help="Time delay")
    parser.add_argument("--bins", type=int, default=100, help="Number of bins for time series")
    args = parser.parse_args()

    with open(args.actor1, "r") as f:
        ts1 = json.load(f)
    with open(args.actor2, "r") as f:
        ts2 = json.load(f)
        
    if not ts1 or not ts2:
        print(json.dumps({"error": "Empty timestamp array(s)"}))
        return

    t_min = min(min(ts1), min(ts2))
    t_max = max(max(ts1), max(ts2))
    
    # If the time span is 0, we can't bin
    if t_min == t_max:
        t_max = t_min + 1
        
    series1 = bin_timestamps(ts1, t_min, t_max, args.bins)
    series2 = bin_timestamps(ts2, t_min, t_max, args.bins)
    
    M1, idx1 = reconstruct_manifold(series1, args.E, args.tau)
    M2, idx2 = reconstruct_manifold(series2, args.E, args.tau)
    
    rho_1_to_2 = ccm_cross_map(M1, idx1, series2, args.E)
    rho_2_to_1 = ccm_cross_map(M2, idx2, series1, args.E)
    
    # Interpretation:
    # If rho(M_x -> Y) > rho(M_y -> X), then Y drives X.
    # Because M_x -> Y means the shadow manifold of X can predict Y, 
    # which implies information about Y is encoded in X, meaning Y causes X.
    
    if rho_1_to_2 > rho_2_to_1 + 0.1:
        direction = "actor2_causes_actor1"
        score = rho_1_to_2
    elif rho_2_to_1 > rho_1_to_2 + 0.1:
        direction = "actor1_causes_actor2"
        score = rho_2_to_1
    else:
        direction = "bidirectional_or_none"
        score = max(rho_1_to_2, rho_2_to_1)
        
    result = {
        "rho_actor1_to_actor2": float(rho_1_to_2),
        "rho_actor2_to_actor1": float(rho_2_to_1),
        "causal_direction": direction,
        "ccm_score": float(score)
    }
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
