import unittest
from typing import List

import pymoo.core.variable

from backend.build.lib.mcd_demo.fit_optimization.const_maps import SEED_BIKES_MAP
from mcd_demo.fit_optimization.bike_optimizers import ErgonomicsOptimizer
from mcd_demo.fit_optimization.optimization_constants import DESIGNS, FEATURES_DATATYPES
from mcd_demo.fit_optimization.seeds_constants import RIDERS_MAP, USED_SEED_BIKES
from mcd_demo.pose_analysis.pose_image_processing import PoserAnalyzer


class McdDemoRegressionTest(unittest.TestCase):
    def setUp(self):
        self.optimizer = ErgonomicsOptimizer(PoserAnalyzer())

    def test_all_riders_pass_all_bikes(self):
        failures = []

        for rider in RIDERS_MAP.keys():
            for seed_bike in USED_SEED_BIKES:
                self._attempt_optimization(failures, rider, seed_bike)

        if len(failures) != 0:
            self.fail(f"There were test failures: {failures}")

    def _attempt_optimization(self, failures: List, rider: str, seed_bike: str):
        try:
            optimized = self.optimizer.optimize_for_seeds(seed_bike_id=seed_bike, rider_id=rider)
            if len(optimized["bikes"]) < 5:
                self._add_failure(failures, rider, seed_bike)
        except Exception as e:
            print(f"Something went wrong {e}")
            self._add_failure(failures, rider, seed_bike)

    def _add_failure(self, failures: List, rider: str, seed_bike: str):
        failures.append({"rider": rider, "seed_bike": seed_bike})

    @unittest.skip
    def _test_invalid_boundaries_in_seeds(self):
        features = DESIGNS.columns
        for feature, data_type in zip(features, FEATURES_DATATYPES):
            for bike_key in USED_SEED_BIKES:
                bike_value = SEED_BIKES_MAP[str(bike_key)]
                if type(data_type) is pymoo.core.variable.Real:
                    if not (data_type.bounds[0] <= bike_value[feature] <= data_type.bounds[1]):
                        print(f"{feature} in {bike_key} has value {bike_value[feature]} "
                              f"which is out of bounds {data_type.bounds}")
