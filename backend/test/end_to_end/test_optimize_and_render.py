import random

from mcd_demo.cad_services.bikeCad_renderer import RenderingService
from mcd_demo.fit_optimization.bike_optimizers import ErgonomicsOptimizer
from mcd_demo.pose_analysis.pose_image_processing import PoserAnalyzer
from test_utils import McdDemoTestCase


class OptimizeAndRenderEndTOEndTest(McdDemoTestCase):
    def setUp(self) -> None:
        self.optimizer = ErgonomicsOptimizer(PoserAnalyzer())
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
            "Invalid seed bike ID [DOES_NOT_EXIST]"
        )

    def test_e2e(self):
        optimized_bikes = self.optimizer.optimize_for_seeds("1", "1")
        self.renderer.render_object(random.choice(optimized_bikes["bikes"])["bike"], "1")
