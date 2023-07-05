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
        dataframe = pd.DataFrame.from_records([bike, bike, bike])
        print(self.analyzer.get_bikes_fit(dataframe.values, body_dimensions))

    def test_get_bike_loss_from_image(self):
        body_dimensions = self.analyzer.get_body_dimensions(75, "resources/image2.jpeg")
        bike = {
            "seat_x": -9,
            "seat_y": 27,
            "handle_bar_x": 16.5,
            "handle_bar_y": 25.5,
            "crank_length": 7,
        }
        bike_fit = self.analyzer.get_bike_fit(bike, body_dimensions)
        self.assertDictAlmostEqual(
            {'knee': 0.220, 'back': 0.004, 'armpit_wrist': 3.70e-06},
            bike_fit
        )

    def assertDictAlmostEqual(self, expected, actual, places=2):
        self.assertEqual(len(expected), len(actual))
        for key, value in actual.items():
            self.assertTrue(key in expected)
            self.assertAlmostEqual(value, expected[key], places=places)
