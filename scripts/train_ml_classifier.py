# LibreFang — train_ml_classifier.py
# Part of fix: Fix 1 — Replace fake ml-classifier with real trained model
# Author: coding-agent
# Date: 2026-06-22

import argparse
import json
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_validate
import joblib

def main():
    parser = argparse.ArgumentParser(description="Train LibreFang ML Classifier")
    parser.add_argument("--data", required=True, help="Path to CSV dataset (columns: text, label)")
    args = parser.parse_args()

    print(f"Loading data from {args.data}...")
    df = pd.read_csv(args.data)
    
    if 'text' not in df.columns or 'label' not in df.columns:
        raise ValueError("Dataset must contain 'text' and 'label' columns.")

    X = df['text'].fillna("")
    y = df['label']

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=50000,
            ngram_range=(1, 3),
            sublinear_tf=True,
            min_df=3
        )),
        ('clf', LogisticRegression(
            C=1.0,
            class_weight='balanced',
            max_iter=1000,
            solver='lbfgs',
            n_jobs=-1
        ))
    ])

    print("Running 5-fold stratified cross-validation...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scoring = ['f1', 'precision', 'recall', 'roc_auc']
    
    cv_results = cross_validate(pipeline, X, y, cv=cv, scoring=scoring, n_jobs=-1)
    
    report = {
        "mean_f1": float(np.mean(cv_results['test_f1'])),
        "mean_precision": float(np.mean(cv_results['test_precision'])),
        "mean_recall": float(np.mean(cv_results['test_recall'])),
        "mean_roc_auc": float(np.mean(cv_results['test_roc_auc']))
    }

    print("\nCross-Validation Results:")
    for metric, value in report.items():
        print(f"  {metric}: {value:.4f}")

    print("\nFitting final model on all data...")
    pipeline.fit(X, y)

    os.makedirs("models", exist_ok=True)
    
    model_path = "models/ml_classifier.joblib"
    report_path = "models/ml_classifier_report.json"
    
    joblib.dump(pipeline, model_path)
    print(f"Model saved to {model_path}")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    main()
