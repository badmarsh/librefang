import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

try:
    import torch
    from tgn_inference import TGNInferenceDummy
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

@unittest.skipIf(not HAS_TORCH, "PyTorch not installed")
class TestTGNInference(unittest.TestCase):
    def setUp(self):
        self.tgn = TGNInferenceDummy(node_features=10, memory_dim=10)

    def test_process_event(self):
        features = torch.ones(10)
        score = self.tgn.process_event("user1", "post1", 1600000000.0, features)
        self.assertTrue(0.0 <= score <= 1.0)
        self.assertIn("user1", self.tgn.memory)
        self.assertIn("post1", self.tgn.memory)
        
    def test_memory_update(self):
        features = torch.zeros(10)
        # Process once
        self.tgn.process_event("user1", "post1", 100.0, features)
        # Check memory
        self.assertGreater(self.tgn.memory["user1"][0].item(), 0.05)
        self.assertGreater(self.tgn.memory["post1"][0].item(), 0.05)

if __name__ == "__main__":
    unittest.main()
