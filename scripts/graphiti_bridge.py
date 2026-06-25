import json
import datetime
import uuid
from typing import Dict, Any, List

class GraphitiBridge:
    """
    Temporal Knowledge Graph bridge for the archivist agent.
    Implements the Zep/Graphiti temporal validity pattern.
    """
    def __init__(self, db_path: str = ":memory:"):
        self.nodes = {}
        self.edges = []
    
    def upsert_node(self, node_id: str, node_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        if node_id in self.nodes:
            old_node = self.nodes[node_id]
            old_node['valid_until'] = now
            old_node['expired_at'] = now
        
        new_node = {
            "id": node_id,
            "type": node_type,
            "valid_from": now,
            "valid_until": None,
            "created_at": now,
            "expired_at": None,
            "data": data
        }
        self.nodes[node_id] = new_node
        return new_node
        
    def add_edge(self, from_id: str, to_id: str, relation: str, properties: Dict[str, Any] = None) -> Dict[str, Any]:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        edge_id = str(uuid.uuid4())
        edge = {
            "id": edge_id,
            "from_id": from_id,
            "to_id": to_id,
            "relation": relation,
            "valid_from": now,
            "valid_until": None,
            "created_at": now,
            "expired_at": None,
            "properties": properties or {}
        }
        self.edges.append(edge)
        return edge

if __name__ == "__main__":
    print("Graphiti Bridge Ready")
