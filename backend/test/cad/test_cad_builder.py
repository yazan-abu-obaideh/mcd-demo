import random

from mcd_demo.cad_services.bike_xml_handler import BikeXmlHandler
from mcd_demo.cad_services.cad_builder import BikeCadFileBuilder, OPTIMIZED_TO_CAD
from test_utils import McdDemoTestCase


class CadBuilderTest(McdDemoTestCase):
    def setUp(self) -> None:
        self.cad_builder = BikeCadFileBuilder()

    def test_builder_cad(self):
        """Verify resulting CAD file contains all required changes..."""
        bike_object_keys = ['HT Length', 'HT Angle', 'HT LX', 'Stack', 'ST Length', 'ST Angle',
                            'Seatpost LENGTH', 'Saddle height', 'Stem length', 'Stem angle', 'Headset spacers',
                            'Crank length', 'Handlebar style']
        bike_object = {key: random.random() for key in bike_object_keys}
        xml_string = self.cad_builder.build_cad_from_object(bike_object,
                                                            "1")
        xml_handler = BikeXmlHandler()
        xml_handler.set_xml(xml_string)
        result_as_dict = xml_handler.get_entries_dict()
        for key, value in bike_object.items():
            self.assertEqual(str(value), result_as_dict[OPTIMIZED_TO_CAD[key]])
