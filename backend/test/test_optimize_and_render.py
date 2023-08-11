import random

from cad_services.bikeCad_renderer import RenderingService
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
                "lower_leg": (22 * 25.4),
                "upper_leg": (22 * 25.4),
                "torso_length": (21 * 25.4),
                "ankle_angle": 105,
                "foot_length": (5.5 * 25.4),
                "arm_length": (24 * 25.4),
                "shoulder_to_wrist": (12 * 25.4),
                "height": (71 * 25.4),
            })
        self.renderer.render_object(random.choice(optimized_bikes["bikes"])["bike"], "1")
