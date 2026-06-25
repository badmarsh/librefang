import os
import json
import torch
from pathlib import Path

# Mocked TGN implementation for Temporal Graph Network CIB detection
class TemporalGraphNetwork:
    def __init__(self, model_path="data/tgn_model/", num_nodes=10000, mem_dim=100, time_dim=100, msg_dim=100):
        self.model_path = Path(model_path)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.is_loaded = self.model_path.exists()
        
        try:
            from torch_geometric.nn.models.tgn import TGNMemory
            from torch_geometric.nn.models.tgn import IdentityMessage
            from torch_geometric.nn.models.tgn import LastAggregator
            
            self.memory = TGNMemory(
                num_nodes=num_nodes,
                raw_msg_dim=msg_dim,
                memory_dim=mem_dim,
                time_dim=time_dim,
                message_module=IdentityMessage(msg_dim, mem_dim, time_dim),
                aggregator_module=LastAggregator(),
            ).to(self.device)
            
            if self.is_loaded:
                # In a real setup, we'd load self.memory.load_state_dict(...)
                pass
        except ImportError:
            self.memory = None
            print("Warning: torch_geometric not installed. TGN models will not function.")
        
        # Simple string hasher for demonstration nodes
        self.node_mapping = {}
        
    def _get_node_id(self, identifier: str) -> int:
        if identifier not in self.node_mapping:
            self.node_mapping[identifier] = len(self.node_mapping)
        return self.node_mapping[identifier]
        
    def predict_coordination_score(self, source_url: str, claim_hash: str, timestamp: str) -> float:
        """
        Returns a coordination probability score between 0.0 and 1.0.
        Uses torch_geometric TGNMemory to evaluate the likelihood of the new edge.
        """
        if self.memory is None:
            return 0.5 # Neutral fallback if no PyG
            
        src_id = self._get_node_id(source_url)
        dst_id = self._get_node_id(claim_hash)
        
        # In a real deployment, we convert timestamp to a relative integer (e.g., minutes since epoch)
        # Here we mock it as a single tensor update
        t = torch.tensor([1], device=self.device)
        src = torch.tensor([src_id], device=self.device)
        dst = torch.tensor([dst_id], device=self.device)
        msg = torch.zeros((1, self.memory.raw_msg_dim), device=self.device)
        
        # Update memory state with the new interaction
        self.memory(src, dst, t, msg)
        
        # Simulated likelihood extraction (real implementation would use a LinkPredictor decoder on the memory)
        score = 0.5
        if "infovojna.sk" in source_url or "hlavnespravy.sk" in source_url:
            score += 0.3
        
        return min(1.0, max(0.0, score))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="TGN CIB Scoring")
    parser.add_argument("--source", type=str, required=True)
    parser.add_argument("--claim_hash", type=str, required=True)
    parser.add_argument("--timestamp", type=str, required=True)
    
    args = parser.parse_args()
    
    tgn = TemporalGraphNetwork()
    score = tgn.predict_coordination_score(args.source, args.claim_hash, args.timestamp)
    print(json.dumps({"tgn_cib_score": score}))
