import unittest
import sys
import os
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

try:
    from graphiti_bridge import GraphitiBridge
except ImportError:
    pass

class TestGraphitiBridge(unittest.TestCase):
    def setUp(self):
        self.bridge = GraphitiBridge()

    def test_node_upsert_temporal_logic(self):
        # Insert first node
        node_id = "test-node-1"
        data1 = {"credibility": 0.5}
        n1 = self.bridge.upsert_node(node_id, "Source", data1)
        
        self.assertIsNone(n1["valid_until"])
        self.assertEqual(n1["data"]["credibility"], 0.5)
        self.assertIsNotNone(n1["valid_from"])
        
        # Upsert with new data
        data2 = {"credibility": 0.2}
        n2 = self.bridge.upsert_node(node_id, "Source", data2)
        
        # In a real temporal DB we would keep the old history object
        # but in this mock, we just assert the new state has valid_until=None
        self.assertIsNone(n2["valid_until"])
        self.assertEqual(n2["data"]["credibility"], 0.2)
        self.assertEqual(n2["id"], "test-node-1")

    def test_add_edge(self):
        edge = self.bridge.add_edge("actor1", "claim1", "MADE", {"platform": "telegram"})
        self.assertEqual(edge["from_id"], "actor1")
        self.assertEqual(edge["to_id"], "claim1")
        self.assertEqual(edge["relation"], "MADE")
        self.assertIsNone(edge["valid_until"])
        self.assertEqual(edge["properties"]["platform"], "telegram")
        self.assertIsNotNone(edge["id"])

if __name__ == "__main__":
    unittest.main()
