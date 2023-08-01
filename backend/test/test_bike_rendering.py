import json
import uuid

from bike_rendering.bikeCad_renderer import BikeCad, RenderingService
from test_utils import McdDemoTestCase


class BikeRendererTest(McdDemoTestCase):
    def test_render_bike(self):
        with BikeCad() as renderer:
            with open(self.resource_path("bike.bcad"), "r") as file:
                self.assertIsNotNone(renderer.render(file.read()))

    def test_render_bike_object(self):
        with open(self.resource_path("optimization_response.txt"), "r") as file:
            optimization_response = json.load(file)
        for bike in optimization_response["bikes"]:
            service = RenderingService(renderer_pool_size=1)
            image = service.render_object(bike)
            with open(f"{str(uuid.uuid4())}.svg", "wb") as file:
                file.write(image)
