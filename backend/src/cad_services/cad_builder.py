import os

from cad_services.bike_xml_handler import BikeXmlHandler
from exceptions import UserInputException

OPTIMIZED_TO_CAD = {
    "ST Angle": "Seat angle",
    "HT Length": "Head tube length textfield",
    "HT Angle": "Head angle",
    "HT LX": "Head tube lower extension2",
    'Stack': 'Stack',
    "ST Length": "Seat tube length",
    "Seatpost LENGTH": "Seatpost LENGTH",
    "Saddle height": "Saddle height",
    "Stem length": "Stem length",
    "Crank length": "Crank length",
    "Headset spacers": "Headset spacers",
    "Stem angle": "Stem angle",
    "Handlebar style": "Handlebar style",
}

SEED_BIKES = {
    "1": "bike1.bcad",
    "2": "bike2.bcad",
    "3": "bike3.bcad"
}


def _get_valid_seed_bike(seed_image_id):
    bike = SEED_BIKES.get(str(seed_image_id))
    if bike is None:
        raise UserInputException("Invalid seed image ID")
    return bike


def _build_bike_path(seed_bike_id):
    seed_image = _get_valid_seed_bike(seed_bike_id)
    return os.path.join(os.path.dirname(__file__), "../resources", "seed-bikes", seed_image)


class BikeCadFileBuilder:
    def build_cad_from_object(self, bike_object, seed_bike_id) -> str:
        xml_handler = BikeXmlHandler()
        self._load_seed_xml(xml_handler, seed_bike_id)
        for response_key, cad_key in OPTIMIZED_TO_CAD.items():
            self._update_xml(xml_handler, bike_object, cad_key, response_key)
        return xml_handler.get_content_string()

    def _load_seed_xml(self, xml_handler, seed_image_id):
        with open(_build_bike_path(seed_image_id), "r") as file:
            xml_handler.set_xml(file.read())

    def _update_xml(self, xml_handler, bike_object, cad_key, response_key):
        entry = xml_handler.find_entry_by_key(cad_key)
        if entry:
            xml_handler.update_entry_value(entry, str(bike_object[response_key]))
        else:
            xml_handler.add_new_entry(cad_key, str(bike_object[response_key]))
