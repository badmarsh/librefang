#!/usr/bin/env python3
"""
scripts/eval_slovak_post2025.py

Evaluates the primary claim-detection models (SlovakBERT, SlavicBERT, XLM-R)
against the post-2025 Slovak disinformation evaluation dataset.
"""

import json
import os
import sys
import requests

EVAL_FILE = "data/post_2025_slovak_disinfo_eval.jsonl"
ML_CLASSIFIER_URL = os.environ.get("ML_CLASSIFIER_URL", "http://127.0.0.1:8090/score")

def main():
    if not os.path.exists(EVAL_FILE):
        print(f"Error: Dataset {EVAL_FILE} not found.")
        sys.exit(1)

    print(f"Loading {EVAL_FILE}...")
    claims = []
    with open(EVAL_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            claims.append(json.loads(line.strip()))

    print(f"Loaded {len(claims)} evaluation samples.")
    print(f"Querying ML Classifier at {ML_CLASSIFIER_URL}...")
    
    correct = 0
    for claim in claims:
        try:
            resp = requests.post(ML_CLASSIFIER_URL, json={"text": claim["text"]}, timeout=5)
            if resp.status_code == 200:
                prediction = resp.json().get("label", "UNCERTAIN")
            else:
                prediction = "UNCERTAIN"
        except requests.exceptions.RequestException:
            prediction = "UNCERTAIN"
            
        if prediction == claim["label"]:
            correct += 1

    accuracy = correct / len(claims) if claims else 0
    print(f"Evaluation complete. Accuracy on post-2025 Slovak dataset: {accuracy:.2%}")
    if accuracy >= 0.70:
        print("Model validation verified.")
    else:
        print("Critical failure: Model is naive to post-2025 vectors.")
        sys.exit(1)

if __name__ == "__main__":
    main()

