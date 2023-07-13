import unittest

from backend.exceptions import UserInputException
from backend.models.ergo_bike import ErgoBike
from backend.models.model_scheme_validations import map_request_to_model


class ModelValidationsTest(unittest.TestCase):
    def test_invalid_type(self):
        with self.assertRaises(UserInputException) as e:
            map_request_to_model({
                "seat_x": None,
                "seat_y": 15,
                "handle_bar_x": 45,
                "handle_bar_y": 35,
                "crank_length": 35
            }, ErgoBike)
        self.assertEqual(e.exception.args[0], "Invalid type for seat_x - expected float")

    def test_missing_parameter(self):
        with self.assertRaises(UserInputException) as e:
            map_request_to_model({"seat_y": 15,
                                  "handle_bar_x": 45,
                                  "handle_bar_y": 35,
                                  "crank_length": 35
                                  }, ErgoBike)
        self.assertEqual(e.exception.args[0], "Required parameter seat_x missing")

    def test_cast_to_validated(self):
        self.assertEqual(ErgoBike(
            seat_x=5,
            seat_y=15,
            handle_bar_x=25,
            handle_bar_y=35,
            crank_length=35,
        ), map_request_to_model({
            "seat_x": 5,
            "seat_y": 15,
            "handle_bar_x": 25,
            "handle_bar_y": 35,
            "crank_length": 35
        },
            ErgoBike))
