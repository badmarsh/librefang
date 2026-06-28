#!/usr/bin/env python3
"""
TGN Inference Script (Mock)
Wave 4 - Temporal Graph Networks anomaly detection.

Reads a JSON graph input and applies a synthetic anomaly probability score
to its edges based on a heuristic, then outputs JSON.
"""

import sys
import json
import random
import argparse

def main():
    parser = argparse.ArgumentParser(description="Mock TGN Inference")
    parser.add_argument("--input", "-i", type=str, required=True, help="Input JSON graph file")
    parser.add_argument("--output", "-o", type=str, required=True, help="Output JSON result file")
    args = parser.parse_args()

    try:
        with open(args.input, "r") as f:
            graph = json.load(f)
    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)

    edges = graph.get("edges", [])
    
    # Heuristic: apply a random anomaly probability, slightly biased by whether the edge has a 'suspicious' flag
    results = []
    for edge in edges:
        base_score = 0.2
        if edge.get("suspicious", False):
            base_score = 0.6
            
        anomaly_prob = min(1.0, max(0.0, base_score + random.uniform(-0.2, 0.4)))
        
        results.append({
            "source": edge.get("source"),
            "target": edge.get("target"),
            "timestamp": edge.get("timestamp"),
            "anomaly_probability": round(anomaly_prob, 4)
        })

    output_data = {
        "status": "success",
        "processed_edges": len(results),
        "results": results
    }

    try:
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)
        print(f"Successfully processed {len(edges)} edges. Results saved to {args.output}")
    except Exception as e:
        print(f"Error writing output: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
