import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

try:
    from adapt_slovakbert import SlovakBERTAdapter
except ImportError:
    pass

class TestSlovakBERTAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = SlovakBERTAdapter()

    def test_dapt_and_tapt(self):
        self.assertFalse(self.adapter.is_adapted)
        success_dapt = self.adapter.run_dapt("dummy_domain_corpus.txt")
        self.assertTrue(success_dapt)
        
        success_tapt = self.adapter.run_tapt("dummy_task_corpus.txt")
        self.assertTrue(success_tapt)
        self.assertTrue(self.adapter.is_adapted)

    def test_init(self):
        self.assertEqual(self.adapter.model_name, "gerulata/slovakbert")

if __name__ == "__main__":
    unittest.main()
