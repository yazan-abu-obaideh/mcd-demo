from bike_rendering.bikeCad_renderer import BikeCAD
from test_utils import McdDemoTestCase


class BikeRendererTest(McdDemoTestCase):
    def test_render_bike(self):
        with BikeCAD() as renderer:
            with open("resources/bike.bcad", "r") as file:
                print(renderer.render(file.read()))
