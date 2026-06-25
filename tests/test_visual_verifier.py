import unittest
from unittest.mock import MagicMock

class MockVLMAPI:
    def verify_image(self, image_data: str, claim_text: str) -> dict:
        # Mocking the Vision-Language Model API
        if "deepfake" in claim_text.lower():
            return {"visual_consistency_score": 0.2, "deepfake_probability": 0.9}
        return {"visual_consistency_score": 0.9, "deepfake_probability": 0.1}

class TestVisualVerifier(unittest.TestCase):
    def setUp(self):
        self.api = MockVLMAPI()

    def test_verify_authentic_image(self):
        result = self.api.verify_image("base64_data...", "This is a normal photo of a protest.")
        self.assertGreater(result["visual_consistency_score"], 0.8)
        self.assertLess(result["deepfake_probability"], 0.2)

    def test_verify_deepfake_image(self):
        result = self.api.verify_image("base64_data...", "This is a deepfake video of the president.")
        self.assertLess(result["visual_consistency_score"], 0.5)
        self.assertGreater(result["deepfake_probability"], 0.8)

if __name__ == "__main__":
    unittest.main()
