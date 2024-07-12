import unittest

from mcd_demo.bike_embedding.clip_embedding_calculator import ClipEmbeddingCalculatorImpl
from mcd_demo.fit_optimization.embedding_similarity_optimizer import optimize_similarity


class EmbeddingSimilarityOptimizerTest(unittest.TestCase):
    def test_does_not_throw(self):
        calculator = ClipEmbeddingCalculatorImpl()
        optimize_similarity(
            target_embedding=calculator.from_text("Red bicycle"),
            pop_size=30,
            n_generations=5,
            sample_from_dataset=False,
            initialize_from_dataset=False,
            maximum_cosine_distance=0.8
        )
