from backend.fit_analysis.fit_analyzer import FitAnalyzer
from test_utils import McdDemoTestCase


class FitAnalyzerTest(McdDemoTestCase):
    def setUp(self) -> None:
        self.analyzer = FitAnalyzer()
        self.body_dimensions = {'height': 75, 'sh_height': 61.09855828510818,
                                'hip_to_ankle': 31.167514055725047, 'hip_to_knee': 15.196207871637029,
                                'shoulder_to_wrist': 13.538605228960089, 'arm_len': 16.538605228960087,
                                'tor_len': 26.931044229383136, 'low_leg': 18.971306184088018,
                                'up_leg': 15.196207871637029}

    def test_multiple_identical_bikes(self):
        bike = {
            "seat_x": -9,
            "seat_y": 27,
            "handle_bar_x": 16.5,
            "handle_bar_y": 25.5,
            "crank_length": 7,
        }
        fits = self.analyzer.get_bikes_fit([bike, bike, bike], self.body_dimensions)
        for fit in fits:
            self.assertDictAlmostEqual(
                {'knee': 0.22047607902399724, 'back': 0.004542793473335416,
                 'armpit_wrist': 3.709120281913947e-06},
                fit
            )

    def test_multiple_bikes(self):
        self.assertDictAlmostEqual(
            {'knee': 0.220, 'back': 0.004, 'armpit_wrist': 3.70e-06},
            self.analyzer.get_bike_fit({
                "seat_x": -9,
                "seat_y": 27,
                "handle_bar_x": 16.5,
                "handle_bar_y": 25.5,
                "crank_length": 7,
            }, self.body_dimensions)
        )
        self.assertDictAlmostEqual(
            {'knee': 0.15836885321815997, 'back': 0.20576194429318562,
             'armpit_wrist': 1.7932198281833678e-08},
            self.analyzer.get_bike_fit({
                "seat_x": -10,
                "seat_y": 24,
                "handle_bar_x": 13.5,
                "handle_bar_y": 29.5,
                "crank_length": 10,
            }, self.body_dimensions)
        )
        self.assertDictAlmostEqual(
            {'knee': 0.009045069976388542, 'back': 4.868244307676406e-08,
             'armpit_wrist': 0.00010221854516923035},
            self.analyzer.get_bike_fit({
                "seat_x": -7,
                "seat_y": 30,
                "handle_bar_x": 18.5,
                "handle_bar_y": 22.5,
                "crank_length": 4,
            }, self.body_dimensions)
        )
