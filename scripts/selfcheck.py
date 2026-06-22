import os
from typing import List, Dict

try:
    import torch
    import spacy
    from selfcheckgpt.modeling_selfcheck import SelfCheckNLI
    HAS_SELFCHECK = True
except ImportError:
    HAS_SELFCHECK = False

class SelfCheckHallucinationDetector:
    def __init__(self, device="cpu"):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.nlp = None
        self.selfcheck_nli = None
        if HAS_SELFCHECK:
            try:
                self.nlp = spacy.load("en_core_web_sm")
                # Using a generic NLI model for SelfCheckGPT
                self.selfcheck_nli = SelfCheckNLI(device=self.device)
            except Exception as e:
                print(f"Warning: SelfCheckNLI initialization failed: {e}")
                HAS_SELFCHECK = False
    
    def evaluate(self, generated_passage: str, sampled_passages: List[str]) -> Dict:
        """
        Evaluate hallucination of the generated_passage using sampled_passages.
        Returns a sentence-level hallucination score and an aggregate document score.
        """
        if not HAS_SELFCHECK or not self.selfcheck_nli:
            return {
                "hallucination_score": 0.1, 
                "sentence_scores": [],
                "status": "mocked_offline"
            }
            
        sentences = [sent.text.strip() for sent in self.nlp(generated_passage).sents if len(sent.text.strip()) > 3]
        if not sentences:
            return {"hallucination_score": 0.0, "sentence_scores": [], "status": "success"}
            
        sent_scores = self.selfcheck_nli.predict(
            sentences=sentences,
            sampled_passages=sampled_passages,
        )
        
        # Aggregate score (average of sentence scores)
        agg_score = sum(sent_scores) / len(sent_scores) if sent_scores else 0.0
        
        return {
            "hallucination_score": agg_score,
            "sentence_scores": sent_scores,
            "status": "success"
        }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SelfCheckGPT Hallucination Detection")
    parser.add_argument("--passage", type=str, required=True, help="The generated passage to verify")
    parser.add_argument("--samples", type=str, nargs='+', required=True, help="Sampled passages for reference")
    
    args = parser.parse_args()
    detector = SelfCheckHallucinationDetector()
    
    result = detector.evaluate(args.passage, args.samples)
    print(result)
