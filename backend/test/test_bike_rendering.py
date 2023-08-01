from bike_rendering.bikeCad_renderer import BikeCad
from test_utils import McdDemoTestCase


class BikeRendererTest(McdDemoTestCase):
    def test_render_bike(self):
        with BikeCad() as renderer:
            with open(self.test_resource_path("bike.bcad"), "r") as file:
                self.assertIsNotNone(renderer.render(file.read()))
