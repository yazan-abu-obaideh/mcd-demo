import os.path

import pandas as pd

from mcd_demo import resource_utils
from mcd_demo.cad_services.bikeCad_renderer import RenderingService
from mcd_demo.cad_services.parametric_to_image_convertor import ParametricToImageConvertor
from test_utils import McdDemoTestCase


class BikeRendererTest(McdDemoTestCase):
    def test_render_bike(self):
        with open(self.resource_path("bike.bcad"), "r") as file:
            self.assertIsNotNone(RenderingService(renderer_pool_size=1).render(file.read()))

    def test_render_bike_object(self):
        # 'HT Length', 'HT LX', 'ST Length'
        bike = {"DT Length": 555.7422710300327, "HT Length": 540.5674859296399, "HT Angle": 73.0,
                "HT LX": 140.89997584848615,
                "Stack": 0.7, "ST Length": 0.25, "ST Angle": 55.34892932796525,
                "Seatpost LENGTH": 0.293, "Saddle height": 0.5,
                "Stem length": 0.8,
                "Stem angle": -11.162277491363763, "Headset spacers": 0.47,
                "Crank length": 0.75,
                "Handlebar style": 2}
        RenderingService(renderer_pool_size=1).render_object(bike, "1")

    def test_render_clips(self):
        convertor = ParametricToImageConvertor()
        data = pd.read_csv(resource_utils.resource_path(os.path.join("clips", "clip_sBIKED_processed.csv")),
                           index_col=0)
        rendering_result = convertor.to_image(target_bike=data.iloc[3])
        with open("image.png", "wb") as file:
            file.write(rendering_result.image)
