import unittest

from mcd_demo.fit_optimization.bike_optimizers import ErgonomicsOptimizer
from mcd_demo.pose_analysis.pose_image_processing import PoserAnalyzer


class EmbeddingSimilarityOptimizerTest(unittest.TestCase):
    def test_does_not_throw(self):
        optimizer = ErgonomicsOptimizer(PoserAnalyzer())
        results = optimizer.optimize_text_prompt({"text_prompt": "yellow bike"})
        self.assertEqual(len(results["bikes"]), 5)
