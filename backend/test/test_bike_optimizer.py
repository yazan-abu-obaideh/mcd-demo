import time
import unittest

from fit_optimization.bike_optimizer import BikeOptimizer
from pose_analysis.pose_image_processing import PoserAnalyzer
from test_utils import McdDemoTestCase


class BikeOptimizerTest(McdDemoTestCase):
    def setUp(self) -> None:
        self.optimizer = BikeOptimizer(PoserAnalyzer())

    def test_get_performances(self):
        pass

    def test_optimize_aero_seeds(self):
        for j in range(1, 4):
            self.optimizer.optimize_aerodynamics_for_seeds("1", j)

    def test_optimize_ergo_seeds(self):
        for j in range(1, 3):
            start = time.time()
            results = self.optimizer.optimize_ergonomics_for_seeds("1", j)
            self.assertEqual(5, len(results["bikes"]))
            self.assertEqual(set(results["bikes"][0].keys()),
                             {"bike", "bikePerformance"})
            self.assertLess(time.time() - start, 6.5)

    def test_optimize_ergo_all_seeds(self):
        for j in range(1, 4):
            results_ergo = self.optimizer.optimize_ergonomics_for_seeds("1", j)
            self.assertEqual(5, len(results_ergo["bikes"]))

    def test_invalid_rider_id(self):
        self.assertRaisesWithMessage(lambda: self.optimizer.optimize_ergonomics_for_seeds(
            "1", "DOES_NOT_EXIST"
        ), "Invalid rider ID [DOES_NOT_EXIST]")

    def test_invalid_seed_id(self):
        with open(self.resource_path("dude.jpeg"), "rb") as file:
            # noinspection PyTypeChecker
            self.assertRaisesWithMessage(
                lambda: self.optimizer.optimize_ergonomics_for_custom_rider("DOES_NOT_EXIST", file.read(), 76, 76),
                "Invalid seed bike ID [DOES_NOT_EXIST]")

    @unittest.skip
    def test_no_hard_coded_dimensions(self):
        pass

    def test_optimize_ergo_custom_rider(self):
        with open(self.resource_path("dude.jpeg"), "rb") as file:
            response = self.optimizer.optimize_ergonomics_for_custom_rider("8", file.read(), 75, 75)
            self.assertEqual(5, len(response["bikes"]))
