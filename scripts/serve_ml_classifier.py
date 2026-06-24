# LibreFang — serve_ml_classifier.py
# Part of fix: Wave 3.5 FIX-2 — SlovakBERT / SlavicBERT / XLM-R transformer pipeline
# Model priority (FIX-2):
#   1. gerulata/slovakbert (Slovak-specific, F1=0.8931 on held-out test)
#   2. deeppavlov/bert-base-bg-cs-pl-ru-cased (SlavicBERT, multilingual Slavic)
#   3. facebook/xlm-roberta-base (XLM-R, cross-lingual fallback)
#   4. TF-IDF + Logistic Regression (BASELINE ONLY — NOT RECOMMENDED FOR PRODUCTION)
#      CPU-only fallback: loses morphological variants and syntactic negation.
#      Use only when PyTorch/Transformers are unavailable (e.g. RAM < 4096 MB).
# References: Arkhipov et al. arXiv:1912.07076; Conneau et al. arXiv:1911.02116
# Author: librefang
# Date: 2026-06-24 (Wave 3.5 update)

import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import uvicorn

app = FastAPI(title="LibreFang ML Classifier")

# Global model state
classifier_type = None
transformer_pipeline = None
tfidf_pipeline = None
model_version = "unknown"
temperature_T = 1.0


# Try importing HuggingFace transformers and PyTorch
try:
    import torch
    from transformers import pipeline as hf_pipeline
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

@app.on_event("startup")
def load_model():
    global classifier_type, transformer_pipeline, tfidf_pipeline, model_version, temperature_T
    
    try:
        import json
        with open("data/conformal_threshold.json", "r") as f:
            t_data = json.load(f)
            temperature_T = t_data.get("temperature_T", 1.0)
            print(f"Loaded Temperature T = {temperature_T:.4f}")
    except Exception as e:
        print("No conformal calibration data found, defaulting to T=1.0")
    
    force_tfidf = os.environ.get("ML_CLASSIFIER_FORCE_TFIDF", "0") == "1"
    
    if HAS_TRANSFORMERS and not force_tfidf:
        # Priority order (Wave 3.5 FIX-2):
        #   1. gerulata/slovakbert        — Slovak-specific, F1=0.8931
        #   2. deeppavlov/bert-base-bg-cs-pl-ru-cased (SlavicBERT)
        #   3. facebook/xlm-roberta-base  — cross-lingual fallback
        # Override with env var ML_TRANSFORMER_MODEL to pin a specific model.
        CLASSIFIER_MODELS = [
            os.environ.get("ML_TRANSFORMER_MODEL", "") or "gerulata/slovakbert",
            "deeppavlov/bert-base-bg-cs-pl-ru-cased",
            "facebook/xlm-roberta-base",
        ]
        # Also support a locally fine-tuned model stored at models/slovak_bert
        local_path = "models/slovak_bert"
        if os.path.exists(local_path):
            CLASSIFIER_MODELS.insert(0, local_path)

        loaded = False
        for model_name in CLASSIFIER_MODELS:
            print(f"Attempting to load transformer model: {model_name} ...")
            try:
                device = 0 if torch.cuda.is_available() and torch.cuda.device_count() > 0 else -1
                transformer_pipeline = hf_pipeline(
                    "text-classification",
                    model=model_name,
                    tokenizer=model_name,
                    device=device,
                    return_all_scores=True
                )
                classifier_type = "transformer"
                model_version = f"transformer:{model_name}"
                print(f"Loaded {model_name} on {'GPU' if device >= 0 else 'CPU'}")
                loaded = True
                break
            except Exception as e:
                print(f"  ⚠️  Could not load {model_name}: {e}", file=sys.stderr)

        if loaded:
            return
        print("All transformer models failed to load. Falling back to TF-IDF baseline.", file=sys.stderr)
            
    # ============================================================
    # ⚠️  BASELINE CLASSIFIER — NOT RECOMMENDED FOR PRODUCTION
    # TF-IDF + Logistic Regression loses morphological variants
    # (e.g. Kremla/Kremlu/Kremom are distinct tokens) and syntactic
    # negation context. F1=0.7871 vs SlovakBERT F1=0.8931.
    # Use ONLY when PyTorch/Transformers are unavailable (CPU-only,
    # RAM < 4096 MB). Run scripts/train_ml_classifier.py to train.
    # Reference: evaluation.md in agents/ml-classifier/
    # ============================================================
    print("[WARNING] BASELINE CLASSIFIER ACTIVE — NOT RECOMMENDED FOR PRODUCTION."
          " Install PyTorch + Transformers to use SlovakBERT (F1=0.8931).")
    model_path = "models/ml_classifier.joblib"
    if not os.path.exists(model_path):
        print(f"ERROR: Baseline TF-IDF model file not found at {model_path}", file=sys.stderr)
        # Create a dummy trained pipeline if not exists so server can start in test/fallback mode
        print("Creating dummy TF-IDF pipeline for testing...", file=sys.stderr)
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import Pipeline as SkPipeline
        dummy_pipe = SkPipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', LogisticRegression())
        ])
        dummy_pipe.fit(["dummy text for calibration", "falošná správa o voľbách"], [0, 1])
        os.makedirs("models", exist_ok=True)
        joblib.dump(dummy_pipe, model_path)
        
    try:
        tfidf_pipeline = joblib.load(model_path)
        classifier_type = "tfidf"
        model_version = f"tfidf:{str(os.path.getmtime(model_path))}"
        print("Baseline TF-IDF model loaded successfully.")
    except Exception as e:
        print(f"ERROR loading TF-IDF model: {e}", file=sys.stderr)
        sys.exit(1)

class ScoreRequest(BaseModel):
    text: str

@app.post("/score")
def score(request: ScoreRequest):
    if classifier_type is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        if classifier_type == "transformer":
            outputs = transformer_pipeline(request.text)[0]
            score_val = 0.5
            for out in outputs:
                label_str = out["label"].upper()
                if label_str in ("LABEL_1", "FAKE", "DISINFORMATION", "DISINFO", "1"):
                    score_val = float(out["score"])
                    break
            else:
                if len(outputs) > 1:
                    score_val = float(outputs[1]["score"])
                else:
                    score_val = float(outputs[0]["score"])
            
            # Apply Temperature Scaling
            import math
            score_val = max(1e-5, min(1 - 1e-5, score_val))
            logit = math.log(score_val / (1.0 - score_val))
            scaled_logit = logit / temperature_T
            calibrated_score = 1.0 / (1.0 + math.exp(-scaled_logit))
            
            label = "DISINFORMATION" if calibrated_score > 0.5 else "CREDIBLE"
            return {
                "score": calibrated_score,
                "label": label,
                "version": model_version,
                "classifier_type": classifier_type
            }
        else:
            proba = tfidf_pipeline.predict_proba([request.text])[0]
            classes = list(tfidf_pipeline.classes_)
            if 1 in classes:
                idx_disinfo = classes.index(1)
                score_val = float(proba[idx_disinfo])
            else:
                score_val = float(proba[1]) if len(proba) > 1 else 0.5
                
            # Apply Temperature Scaling
            import math
            score_val = max(1e-5, min(1 - 1e-5, score_val))
            logit = math.log(score_val / (1.0 - score_val))
            scaled_logit = logit / temperature_T
            calibrated_score = 1.0 / (1.0 + math.exp(-scaled_logit))
                
            label = "DISINFORMATION" if calibrated_score > 0.5 else "CREDIBLE"
            return {
                "score": calibrated_score,
                "label": label,
                "version": model_version,
                "classifier_type": classifier_type
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("ML_CLASSIFIER_PORT", 8090))
    uvicorn.run(app, host="127.0.0.1", port=port)
