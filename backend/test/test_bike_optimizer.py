from fit_optimization.bike_optimizer import BikeOptimizer
from models.body_dimensions import BodyDimensions
from models.ergo_bike import ErgoBike
from pose_analysis.pose_image_processing import PoserAnalyzer
from test_utils import McdDemoTestCase


class BikeOptimizerTest(McdDemoTestCase):
    def setUp(self) -> None:
        self.optimizer = BikeOptimizer(PoserAnalyzer())

    def test_invalid_seed_id(self):
        # noinspection PyTypeChecker
        self.assertRaisesWithMessage(lambda: self.optimizer.optimize_seed_bike(
            "DOES_NOT_EXIST", b"", None, None), "Invalid seed bike ID")

    def test_optimize(self):
        """We need to reliably generate n bikes..."""
        optimized_bikes = self.optimizer.optimize(
            seed_bike=ErgoBike(seat_x=-9, seat_y=27, handle_bar_x=16.5, handle_bar_y=25.5, crank_length=7),
            user_dimensions=BodyDimensions(height=75, sh_height=61.09855828510818, hip_to_ankle=31.167514055725047,
                                           hip_to_knee=15.196207871637029, shoulder_to_wrist=13.538605228960089,
                                           arm_len=16.538605228960087, tor_len=26.931044229383136,
                                           low_leg=18.971306184088018, up_leg=15.196207871637029))
        self.assertGreaterEqual(len(optimized_bikes["bikes"]), 3)
