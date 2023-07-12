import pandas as pd

from backend.fit_analysis.fit_analyzer import FitAnalyzer
from test_utils import McdDemoTestCase


class FitAnalyzerTest(McdDemoTestCase):
    def setUp(self) -> None:
        self.analyzer = FitAnalyzer()
        self.dimensions = {'height': 75, 'sh_height': 61.09855828510818, 'hip_to_ankle': 31.167514055725047,
                           'hip_to_knee': 15.196207871637029, 'shoulder_to_wrist': 13.538605228960089,
                           'arm_len': 16.538605228960087, 'tor_len': 26.931044229383136, 'low_leg': 18.971306184088018,
                           'up_leg': 15.196207871637029}

    def test_multiple_bikes(self):
        bike = {
            "seat_x": -9,
            "seat_y": 27,
            "handle_bar_x": 16.5,
            "handle_bar_y": 25.5,
            "crank_length": 7,
        }
        print(pd.DataFrame.from_records(self.analyzer.get_bikes_fit([bike, bike, bike],
                                                                    self.dimensions)))

    def test_get_bike_loss_from_image(self):
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
        bike_fit = self.analyzer.get_bike_fit(bike, self.dimensions)
        second_fit = self.analyzer.get_bike_fit(second_bike, self.dimensions)
        third_fit = self.analyzer.get_bike_fit(third_bike, self.dimensions)
        self.assertDictAlmostEqual(
            {'knee': 0.220, 'back': 0.004, 'armpit_wrist': 3.70e-06},
            bike_fit
        )
        print(second_fit)
        print(third_fit)
