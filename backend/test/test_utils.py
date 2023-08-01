import os.path
from unittest import TestCase

from exceptions import UserInputException


class McdDemoTestCase(TestCase):

    def assertDictAlmostEqual(self, expected, actual, places=2):
        self.assertEqual(len(expected), len(actual))
        for key, value in actual.items():
            self.assertTrue(key in expected)
            self.assertAlmostEqual(value, expected[key], places=places)

    def assertRaisesWithMessage(self, faulty_call: callable, exception_message):
        with self.assertRaises(expected_exception=UserInputException) as context:
            faulty_call()
        self.assertEqual(exception_message, context.exception.args[0])

    def test_resource_path(self, resource_name):
        return os.path.join(os.path.dirname(__file__), "resources", resource_name)
