import time
import unittest

from fit_optimization.bike_optimizer import BikeOptimizer
from pose_analysis.pose_image_processing import PoserAnalyzer
from test_utils import McdDemoTestCase


class BikeOptimizerTest(McdDemoTestCase):
    def setUp(self) -> None:
        self.optimizer = BikeOptimizer(PoserAnalyzer())

    def test_optimize_seeds(self):
        for j in range(1, 4):
            results = self.optimizer.optimize_ergonomics_for_seeds("1", j)
            self.assertEqual(5, len(results["bikes"]))

    def test_invalid_rider_id(self):
        self.assertRaisesWithMessage(lambda: self.optimizer.optimize_ergonomics_for_seeds(
            "1", "DOES_NOT_EXIST"
        ), "Invalid rider ID [DOES_NOT_EXIST]")

    def test_invalid_seed_id(self):
        # noinspection PyTypeChecker
        self.assertRaisesWithMessage(lambda: self.optimizer.optimize_ergonomics_for_custom_rider(
            "DOES_NOT_EXIST", b"", None, None), "Invalid seed bike ID")

    @unittest.skip
    def test_no_hard_coded_dimensions(self):
        pass

    def test_optimize_by_seed_id(self):
        with open(self.resource_path("dude.jpeg"), "rb") as file:
            response = self.optimizer.optimize_ergonomics_for_custom_rider("15", file.read(), 75, 75)
            self.assertEqual(5, len(response["bikes"]))

    def _test_reliability(self):
        for i in range(25):
            self.test_optimize()
            print(i)

    def test_optimize(self):
        """We need to reliably generate n bikes..."""
        start = time.time()
        optimization_response = self.optimizer._optimize(
            seed_bike={
                "DT Length": 664.021,
                "HT Length": 135.6,
                "HT Angle": 73.0,
                "HT LX": 50.0,
                "Stack": 565.6,
                "ST Length": 588.7,
                "ST Angle": 72.5,
                "Seatpost LENGTH": 300.0,
                "Saddle height": 768.0,
                "Stem length": 120.0,
                "Stem angle": -10.0,
                "Headset spacers": 15.0,
                "Crank length": 172.5,
                "Handlebar style": 0,
            },
            user_dimensions={
                "lower_leg": (22 * 25.4),
                "upper_leg": (22 * 25.4),
                "torso_length": (21 * 25.4),
                "ankle_angle": 105,
                "foot_length": (5.5 * 25.4),
                "arm_length": (24 * 25.4),
                "shoulder_to_wrist": (12 * 25.4),
                "height": (71 * 25.4),
            },
            prediction_function=self.optimizer._predict_ergonomics)
        self.assertEqual(len(optimization_response["bikes"]), 5)
        self.assertEqual(set(optimization_response["bikes"][0].keys()),
                         {"bike", "bikePerformance"})
        self.assertLess(time.time() - start, 5)
