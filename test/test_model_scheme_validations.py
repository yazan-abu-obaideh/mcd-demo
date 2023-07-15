import unittest

from exceptions import UserInputException
from models.ergo_bike import ErgoBike
from models.model_scheme_validations import map_request_to_model


class ModelValidationsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.base_request = {
            "seat_x": 5,
            "seat_y": 15,
            "handle_bar_x": 25,
            "handle_bar_y": 35,
            "crank_length": 35
        }

    def test_invalid_type(self):
        # noinspection PyTypedDict
        self.base_request["seat_x"] = "THING"
        with self.assertRaises(UserInputException) as e:
            map_request_to_model(self.base_request, ErgoBike)
        self.assertEqual(e.exception.args[0], "Invalid type for seat_x - expected float")

    def test_missing_parameter(self):
        request = self.base_request
        del request["seat_x"]
        with self.assertRaises(UserInputException) as e:
            map_request_to_model(self.base_request, ErgoBike)
        self.assertEqual(e.exception.args[0], "Required parameter seat_x missing")

    def test_ignores(self):
        self.base_request["seat_z"] = 355
        self.base_request["MORE"] = "STUFF"
        self.assertEqual(ErgoBike(
            seat_x=5,
            seat_y=15,
            handle_bar_x=25,
            handle_bar_y=35,
            crank_length=35,
        ), map_request_to_model(self.base_request, ErgoBike))

    def test_cast_to_validated(self):
        self.assertEqual(ErgoBike(
            seat_x=5,
            seat_y=15,
            handle_bar_x=25,
            handle_bar_y=35,
            crank_length=35,
        ), map_request_to_model(self.base_request, ErgoBike))

    def test_handles_non_dicts(self):
        with self.assertRaises(UserInputException) as e:
            # noinspection PyTypeChecker
            map_request_to_model(15, ErgoBike)
        self.assertEqual(e.exception.args[0], "Expected json, got 15 instead")
