import random

from bike_rendering.bikeCad_renderer import RenderingService
from fit_optimization.bike_optimizer import BikeOptimizer
from pose_analysis.pose_image_processing import PoserAnalyzer
from test_utils import McdDemoTestCase


class OptimizeAndRenderEndTOEndTest(McdDemoTestCase):
    def setUp(self) -> None:
        self.optimizer = BikeOptimizer(PoserAnalyzer())
        self.renderer = RenderingService(renderer_pool_size=1)

    def test_invalid_seed_image(self):
        self.assertRaisesWithMessage(
            lambda: self.renderer.render_object({
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
            }, "DOES_NOT_EXIST"),
            "Invalid seed image ID"
        )

    def test_e2e(self):
        LL = 22 * 25.4
        UL = 22 * 25.4
        TL = 21 * 25.4
        AL = 24 * 25.4
        FL = 5.5 * 25.4
        AA = 105
        SW = 12 * 25.4
        HT = 71 * 25.4
        optimized_bikes = self.optimizer.optimize(
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
                "lower_leg": LL,
                "upper_leg": UL,
                "torso_length": TL,
                "ankle_angle": AA,
                "foot_length": FL,
                "arm_length": AL,
                "shoulder_to_wrist": SW,
                "height": HT,
            })
        self.renderer.render_object(random.choice(optimized_bikes["bikes"]), "1")
