import os

import pandas as pd

from mcd_demo.cad_services.bikeCad_renderer import ONE_HOT_ENCODED_CLIPS_COLUMNS
from mcd_demo.cad_services.bike_xml_handler import BikeXmlHandler
from mcd_demo.cad_services.clips_to_bcad import clips_to_cad
from mcd_demo.exceptions import UserInputException
from mcd_demo.resource_utils import resource_path, STANDARD_BIKE_RESOURCE

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


def one_hot_decode(bike: pd.Series) -> dict:
    result = {}
    for encoded_value in ONE_HOT_ENCODED_CLIPS_COLUMNS:
        for column in bike.index:
            if encoded_value in column and bike[column] == 1:
                result[encoded_value] = column.split('OHCLASS:')[1].strip()
    return result


def _get_valid_seed_bike(seed_image_id):
    if str(seed_image_id) not in [str(_) for _ in range(1, 14)]:
        raise UserInputException(f"Invalid seed bike ID [{seed_image_id}]")
    return f"bike{seed_image_id}.bcad"


def _build_bike_path(seed_bike_id):
    seed_image = _get_valid_seed_bike(seed_bike_id)
    return os.path.join(os.path.dirname(__file__), "../resources", "seed-bikes", seed_image)


class BikeCadFileBuilder:
    def build_cad_from_object(self, bike_object, seed_bike_id) -> str:
        xml_handler = BikeXmlHandler()
        self._load_seed_xml(xml_handler, seed_bike_id)
        for response_key, cad_key in OPTIMIZED_TO_CAD.items():
            self._update_xml(xml_handler, cad_key, bike_object[response_key])
        # self._update_xml(xml_handler, "Display RIDER", "true")
        return xml_handler.get_content_string()

    def build_cad_from_clips_object(self, target_bike) -> str:
        xml_handler = self._build_xml_handler()
        target_dict = self._to_cad_dict(target_bike)
        self._update_values(xml_handler, target_dict)
        return xml_handler.get_content_string()

    def _build_xml_handler(self):
        xml_handler = BikeXmlHandler()
        self._read_standard_bike_xml(xml_handler)
        return xml_handler

    def _read_standard_bike_xml(self, handler):
        with open(resource_path(STANDARD_BIKE_RESOURCE)) as file:
            handler.set_xml(file.read())

    def _to_cad_dict(self, bike: dict):
        bike_complete = clips_to_cad(pd.DataFrame.from_records([bike])).iloc[0]
        decoded_values = one_hot_decode(bike_complete)
        bike_dict = bike_complete.to_dict()
        bike_dict.update(decoded_values)
        return self._remove_encoded_values(bike_dict)

    def _load_seed_xml(self, xml_handler, seed_image_id):
        with open(_build_bike_path(seed_image_id), "r") as file:
            xml_handler.set_xml(file.read())

    def _update_xml(self, xml_handler, cad_key, desired_value):
        entry = xml_handler.find_entry_by_key(cad_key)
        if entry:
            xml_handler.update_entry_value(entry, str(desired_value))
        else:
            xml_handler.add_new_entry(cad_key, str(desired_value))

    def _remove_encoded_values(self, bike_dict: dict) -> dict:
        to_delete = []
        for k, _ in bike_dict.items():
            for encoded_key in ONE_HOT_ENCODED_CLIPS_COLUMNS:
                if "OHCLASS" in k and encoded_key in k:
                    print(f"Deleting key {k}")
                    to_delete.append(k)
        return {
            k: v for k, v in bike_dict.items() if k not in to_delete
        }

    def _update_values(self, handler, bike_dict):
        num_updated = 0
        for k, v in bike_dict.items():
            parsed = self._parse(v)
            if parsed is not None:
                num_updated += 1
                self._update_value(parsed, handler, k)
        print(f"{num_updated=}")

    def _parse(self, v):
        handled = self._handle_numeric(v)
        handled = self._handle_bool(str(handled))
        return handled

    def _update_value(self, handled, xml_handler, k):
        print(f"Updating {k} with value {handled}")
        xml_handler.add_or_update(k, handled)

    def _handle_numeric(self, v):
        if str(v).lower() == 'nan':
            return None
        if type(v) in [int, float]:
            v = int(v)
        return v

    def _handle_bool(self, param):
        if param.lower().title() in ['True', 'False']:
            return param.lower()
        return param
