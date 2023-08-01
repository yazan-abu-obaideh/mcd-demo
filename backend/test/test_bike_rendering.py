from bike_rendering.bikeCad_renderer import BikeCad, RenderingService
from test_utils import McdDemoTestCase


class BikeRendererTest(McdDemoTestCase):
    def test_render_bike(self):
        with BikeCad() as renderer:
            with open(self.resource_path("bike.bcad"), "r") as file:
                self.assertIsNotNone(renderer.render(file.read()))

    def test_render_bike_object(self):
        service = RenderingService(renderer_pool_size=1)
        service.render_object(
            {}
        )
