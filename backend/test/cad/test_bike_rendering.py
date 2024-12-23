from mcd_demo.cad_services.bikeCad_renderer import RenderingService
from mcd_demo_test_case import McdDemoTestCase

SAMPLE_BIKE_OBJECT = {"DT Length": 555.7422710300327, "HT Length": 540.5674859296399, "HT Angle": 73.0,
                      "HT LX": 140.89997584848615,
                      "Stack": 0.7, "ST Length": 0.25, "ST Angle": 55.34892932796525,
                      "Seatpost LENGTH": 0.293, "Saddle height": 0.5,
                      "Stem length": 0.8,
                      "Stem angle": -11.162277491363763, "Headset spacers": 0.47,
                      "Crank length": 0.75,
                      "Handlebar style": 2}


class BikeRendererTest(McdDemoTestCase):

    def setUp(self):
        self.renderer = RenderingService(renderer_pool_size=1)

    def test_render_bike(self):
        with open(self.resource_path("bike.bcad"), "r") as file:
            self.assertIsNotNone(self.renderer.render(file.read()))

    def test_invalid_seed_image(self):
        self.assertRaisesWithMessage(
            lambda: self.renderer.render_object(SAMPLE_BIKE_OBJECT, "DOES_NOT_EXIST"),
            "Invalid seed bike ID [DOES_NOT_EXIST]"
        )

    def test_render_bike_object(self):
        # 'HT Length', 'HT LX', 'ST Length'
        self.renderer.render_object(SAMPLE_BIKE_OBJECT, "1")
