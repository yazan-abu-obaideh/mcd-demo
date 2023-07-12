import unittest

import numpy as np
import pandas as pd

from backend.pose_image_processing import PoserAnalyzer


class ImageAnalyzerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.analyzer = PoserAnalyzer()

    def test_get_body_dimensions_from_image(self):
        analysis = self.analyzer.get_body_dimensions(75, "resources/image2.jpeg")
        self.assertDictAlmostEqual(
            {'height': 75, 'sh_height': 61.098, 'hip_to_ankle': 31.167,
             'hip_to_knee': 15.196, 'shoulder_to_wrist': 13.538,
             'arm_len': 16.538, 'tor_len': 26.931,
             'low_leg': 18.971, 'up_leg': 15.196},
            analysis
        )

    def test_multiple_bikes(self):
        body_dimensions = self.analyzer.get_body_dimensions(75, "resources/image2.jpeg")
        bike = {
            "seat_x": -9,
            "seat_y": 27,
            "handle_bar_x": 16.5,
            "handle_bar_y": 25.5,
            "crank_length": 7,
        }
        print(pd.DataFrame.from_records(self.analyzer.get_bikes_fit([bike, bike, bike], body_dimensions)))

    def test_get_bike_loss_from_image(self):
        body_dimensions = self.analyzer.get_body_dimensions(75, "resources/image2.jpeg")
        bike = {
            "seat_x": -9,
            "seat_y": 27,
            "handle_bar_x": 16.5,
            "handle_bar_y": 25.5,
            "crank_length": 7,
        }
        second_bike = {
            "seat_x": -10,
            "seat_y": 24,
            "handle_bar_x": 13.5,
            "handle_bar_y": 29.5,
            "crank_length": 10,
        }
        third_bike = {
            "seat_x": -13,
            "seat_y": 30,
            "handle_bar_x": 18.5,
            "handle_bar_y": 22.5,
            "crank_length": 4,
        }
        bike_fit = self.analyzer.get_bike_fit(bike, body_dimensions)
        second_fit = self.analyzer.get_bike_fit(second_bike, body_dimensions)
        third_fit = self.analyzer.get_bike_fit(third_bike, body_dimensions)
        self.assertDictAlmostEqual(
            {'knee': 0.220, 'back': 0.004, 'armpit_wrist': 3.70e-06},
            bike_fit
        )
        print(second_fit)
        print(third_fit)

    def assertDictAlmostEqual(self, expected, actual, places=2):
        self.assertEqual(len(expected), len(actual))
        for key, value in actual.items():
            self.assertTrue(key in expected)
            self.assertAlmostEqual(value, expected[key], places=places)
