# LibreFang — serve_ml_classifier.py
# Part of fix: Fix 1 — Replace fake ml-classifier with real trained model
# Author: coding-agent
# Date: 2026-06-22

import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import uvicorn

app = FastAPI(title="LibreFang ML Classifier")

model_path = "models/ml_classifier.joblib"
pipeline = None
model_version = "unknown"

@app.on_event("startup")
def load_model():
    global pipeline
    global model_version
    if not os.path.exists(model_path):
        print(f"ERROR: Model file not found at {model_path}", file=sys.stderr)
        print("Please run scripts/train_ml_classifier.py first to train the model.", file=sys.stderr)
        sys.exit(1)
    
    try:
        pipeline = joblib.load(model_path)
        model_version = str(os.path.getmtime(model_path))
        print("Model loaded successfully.")
    except Exception as e:
        print(f"ERROR loading model: {e}", file=sys.stderr)
        sys.exit(1)

class ScoreRequest(BaseModel):
    text: str

@app.post("/score")
def score(request: ScoreRequest):
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Get probability for class 1 (DISINFORMATION)
    # Ensure probabilities are extracted properly
    try:
        proba = pipeline.predict_proba([request.text])[0]
        # Assuming classes are 0=credible, 1=disinformation per dataset requirement
        classes = list(pipeline.classes_)
        if 1 in classes:
            idx_disinfo = classes.index(1)
            score_val = float(proba[idx_disinfo])
        else:
            # Fallback if classes are strings or different
            score_val = float(proba[1]) if len(proba) > 1 else 0.5
            
        label = "DISINFORMATION" if score_val > 0.5 else "CREDIBLE"
        
        return {
            "score": score_val,
            "label": label,
            "version": model_version
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("ML_CLASSIFIER_PORT", 8090))
    uvicorn.run(app, host="127.0.0.1", port=port)
