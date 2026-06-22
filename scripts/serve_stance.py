import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Stance Detection Service", version="1.0.0")

class StanceRequest(BaseModel):
    claim: str
    evidence: List[str]

class StanceResponse(BaseModel):
    stance: str
    confidence: float
    stance_scores: dict

@app.post("/predict_stance", response_model=StanceResponse)
def predict_stance(req: StanceRequest):
    # Mocking BGE-M3 cross-encoder logic for stance detection
    # In a real implementation, we would use sentence-transformers CrossEncoder
    
    # Simple mocked logic based on text overlap
    claim_lower = req.claim.lower()
    
    supports_score = 0.1
    refutes_score = 0.1
    unrelated_score = 0.5
    
    for ev in req.evidence:
        ev_lower = ev.lower()
        if "falošné" in ev_lower or "nepravdivé" in ev_lower or "hoax" in ev_lower:
            refutes_score += 0.4
        elif any(word in ev_lower for word in claim_lower.split() if len(word) > 4):
            supports_score += 0.3
            unrelated_score -= 0.2
            
    # Normalize
    total = supports_score + refutes_score + unrelated_score
    supports_score /= total
    refutes_score /= total
    unrelated_score /= total
    
    if supports_score > refutes_score and supports_score > unrelated_score:
        stance = "SUPPORTS"
        confidence = supports_score
    elif refutes_score > supports_score and refutes_score > unrelated_score:
        stance = "REFUTES"
        confidence = refutes_score
    else:
        stance = "UNRELATED"
        confidence = unrelated_score
        
    return StanceResponse(
        stance=stance,
        confidence=confidence,
        stance_scores={
            "SUPPORTS": supports_score,
            "REFUTES": refutes_score,
            "UNRELATED": unrelated_score,
            "NOT_ENOUGH_INFO": 0.0
        }
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("STANCE_PORT", 8002))
    uvicorn.run(app, host="127.0.0.1", port=port)
