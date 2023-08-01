import attrs

from exceptions import UserInputException
from models.model_scheme_validations import map_request_to_model, map_base64_image_to_bytes
from test_utils import McdDemoTestCase


@attrs.define(frozen=True)
class Bike:
    seat_x: float
    seat_y: float
    handle_bar_x: float
    handle_bar_y: float
    crank_length: float


class ModelValidationsTest(McdDemoTestCase):
    def setUp(self) -> None:
        self.base_request = {
            "seat_x": 5,
            "seat_y": 15,
            "handle_bar_x": 25,
            "handle_bar_y": 35,
            "crank_length": 35
        }

    def test_map_invalid_base64_to_bytes(self):
        self.assertRaisesWithMessage(
            lambda: self.assertEqual("", map_base64_image_to_bytes("K")),
            "Invalid image"
        )

    def test_map_to_bytes(self):
        self.assertEqual(b'01010101', map_base64_image_to_bytes("MDEwMTAxMDE="))

    def test_invalid_type(self):
        # noinspection PyTypedDict
        self.base_request["seat_x"] = "THING"
        with self.assertRaises(UserInputException) as e:
            map_request_to_model(self.base_request, Bike)
        self.assertEqual(e.exception.args[0], "Invalid type for seat_x - expected float")

    def test_missing_parameter(self):
        request = self.base_request
        del request["seat_x"]
        with self.assertRaises(UserInputException) as e:
            map_request_to_model(self.base_request, Bike)
        self.assertEqual(e.exception.args[0], "Required parameter seat_x missing")

    def test_ignores(self):
        self.base_request["seat_z"] = 355
        self.base_request["MORE"] = "STUFF"
        self.assertEqual(Bike(
            seat_x=5,
            seat_y=15,
            handle_bar_x=25,
            handle_bar_y=35,
            crank_length=35,
        ), map_request_to_model(self.base_request, Bike))

    def test_cast_to_validated(self):
        self.assertEqual(Bike(
            seat_x=5,
            seat_y=15,
            handle_bar_x=25,
            handle_bar_y=35,
            crank_length=35,
        ), map_request_to_model(self.base_request, Bike))

    def test_handles_non_dicts(self):
        # noinspection PyTypeChecker
        self.assertRaisesWithMessage(lambda: map_request_to_model(15, Bike),
                                     "Expected json, got 15 instead")
