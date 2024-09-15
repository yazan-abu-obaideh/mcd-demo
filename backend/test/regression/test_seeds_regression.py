import unittest
from typing import List

from mcd_demo.fit_optimization.bike_optimizers import ErgonomicsOptimizer, BikeOptimizer, AerodynamicsOptimizer
from mcd_demo.fit_optimization.seeds_constants import RIDERS_MAP, USED_SEED_BIKES
from mcd_demo.pose_analysis.pose_image_processing import PoserAnalyzer


class McdDemoRegressionTest(unittest.TestCase):
    def setUp(self):
        poser_analyzer = PoserAnalyzer()
        self.ergonomics_optimizer = ErgonomicsOptimizer(poser_analyzer)
        self.aerodynamics_optimizer = AerodynamicsOptimizer(poser_analyzer)

    def test_ergonomics_all_riders_pass_all_bikes(self):
        self._test_all_riders_pass(self.ergonomics_optimizer)

    def test_aerodynamics_all_riders_pass_all_bikes(self):
        self._test_all_riders_pass(self.aerodynamics_optimizer)

    def _test_all_riders_pass(self, optimizer: BikeOptimizer):
        failures: List[str] = []
        for rider in RIDERS_MAP.keys():
            for seed_bike in USED_SEED_BIKES:
                self._attempt_optimization(optimizer, failures, rider, seed_bike)
        if len(failures) != 0:
            self.fail(f"Found failures: {failures}")

    def _attempt_optimization(self,
                              optimizer: BikeOptimizer,
                              failures: List[str],
                              rider: str,
                              seed_bike: str):
        try:
            optimized = optimizer.optimize_for_seeds(seed_bike_id=seed_bike, rider_id=rider)
            number_found = len(optimized["bikes"])
            if number_found < 5:
                failures.append(f"Only {number_found} bikes found for rider {rider} and seed bike {seed_bike}")
        except Exception as e:
            failures.append(f"Exception raised by rider {rider} and seed bike {seed_bike}: {e}")
