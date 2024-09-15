import random

from mcd_demo.cad_services.bikeCad_renderer import RenderingService
from mcd_demo.fit_optimization.bike_optimizers import ErgonomicsOptimizer
from mcd_demo.pose_analysis.pose_image_processing import PoserAnalyzer
from mcd_demo_test_case import McdDemoTestCase


class OptimizeAndRenderEndTOEndTest(McdDemoTestCase):
    def setUp(self) -> None:
        self.optimizer = ErgonomicsOptimizer(PoserAnalyzer())
        self.renderer = RenderingService(renderer_pool_size=1)

    def test_seeds_e2e(self):
        optimized_bikes = self.optimizer.optimize_for_seeds("1", "1")
        self.renderer.render_object(random.choice(optimized_bikes["bikes"])["bike"], "1")

    def test_clip_e2e(self):
        optimized_bikes = self.optimizer.optimize_text_prompt({"text_prompt": "A yellow bike"})
        self.renderer.render_clips(random.choice(optimized_bikes["bikes"])["bike"])
