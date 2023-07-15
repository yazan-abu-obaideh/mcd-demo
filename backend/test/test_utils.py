from unittest import TestCase


class McdDemoTestCase(TestCase):

    def assertDictAlmostEqual(self, expected, actual, places=2):
        self.assertEqual(len(expected), len(actual))
        for key, value in actual.items():
            self.assertTrue(key in expected)
            self.assertAlmostEqual(value, expected[key], places=places)
