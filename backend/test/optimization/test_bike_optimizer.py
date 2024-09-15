import unittest

import pymoo

from mcd_demo.fit_optimization.bike_optimizers import *
from mcd_demo.fit_optimization.seeds_constants import USED_SEED_BIKES
from mcd_demo.pose_analysis.pose_image_processing import PoserAnalyzer
from test_utils import McdDemoTestCase


class BikeOptimizerTest(McdDemoTestCase):
    def setUp(self) -> None:
        self.ergo_optimizer = ErgonomicsOptimizer(PoserAnalyzer())
        self.aero_optimizer = AerodynamicsOptimizer(PoserAnalyzer())

    def test_optimize_from_text_prompt(self):
        result = self.aero_optimizer.optimize_text_prompt({
            "text_prompt": "Cool green bike"
        })
        print(len(result))

    def test_get_performances(self):
        pass

    def test_real_boundaries_in_seeds(self):
        invalid = []
        features = DESIGNS.columns
        for feature, data_type in zip(features, FEATURES_DATATYPES):
            for bike_key in USED_SEED_BIKES:
                bike_value = SEED_BIKES_MAP[str(bike_key)]
                if type(data_type) is pymoo.core.variable.Real:
                    if not (data_type.bounds[0] <= bike_value[feature] <= data_type.bounds[1]):
                        invalid.append(f"{feature} in {bike_key} has value {bike_value[feature]} "
                                       f"which is out of bounds {data_type.bounds}")
        if len(invalid) != 0:
            self.fail(f"Found out of bound features: {invalid}")

    def _test_rider_reliability(self):
        total_results = {}
        for rider_id in ["1", "2", "3"]:
            rider_results = {}
            for bike_id in ["1", "2", "3", "11", "5", "6", "7", "10", "12"]:
                ergo_results = self.ergo_optimizer.optimize_for_seeds(bike_id, rider_id)
                aero_results = self.aero_optimizer.optimize_for_seeds(bike_id, rider_id)
                ergo_len = len(ergo_results["bikes"])
                aero_len = len(aero_results["bikes"])
                print(f"Rider {rider_id}, bike {bike_id}. Ergo {ergo_len}, Aero {aero_len}")
                rider_results[bike_id] = {
                    "ergo": ergo_len,
                    "aero": aero_len
                }
            print(rider_results)
            total_results[rider_id] = rider_results
        print(total_results)

    def test_optimize_ergo_seeds(self):
        for j in range(1, 3):
            results = self.ergo_optimizer.optimize_for_seeds("1", str(j))
            self.assertEqual(5, len(results["bikes"]))
            self.assertEqual(set(results["bikes"][0].keys()),
                             {"bike", "bikePerformance"})

    def test_invalid_rider_id(self):
        self.assertRaisesWithMessage(lambda: self.ergo_optimizer.optimize_for_seeds(
            "1", "DOES_NOT_EXIST"
        ), "Invalid rider ID [DOES_NOT_EXIST]")

    def test_invalid_seed_id(self):
        with open(self.resource_path("dude.jpeg"), "rb") as file:
            # noinspection PyTypeChecker
            self.assertRaisesWithMessage(
                lambda: self.aero_optimizer.optimize_for_image("DOES_NOT_EXIST", file.read(), 76),
                "Invalid seed bike ID [DOES_NOT_EXIST]")

    @unittest.skip
    def test_no_hard_coded_dimensions(self):
        pass

    def test_optimize_ergo_custom_rider(self):
        with open(self.resource_path("dude.jpeg"), "rb") as file:
            response = self.ergo_optimizer.optimize_for_image("8", file.read(), 75)
            self.assertEqual(5, len(response["bikes"]))
