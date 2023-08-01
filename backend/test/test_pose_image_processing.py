from pose_analysis.pose_image_processing import PoserAnalyzer
from test_utils import McdDemoTestCase


class ImageAnalyzerTest(McdDemoTestCase):
    def setUp(self) -> None:
        self.analyzer = PoserAnalyzer()

    def test_analyze_invalid_image(self):
        self.assertRaisesWithMessage(
            lambda: self.analyzer.analyze_bytes(75, b"RANDOM_GARBAGE_NOT_AN_IMAGE"),
            "Unknown image file format. One of JPEG, PNG, GIF, BMP required."
        )

    def test_analyze_bytes(self):
        with open("resources/image2.jpeg", "rb") as file:
            self.assertDictAlmostEqual(
                {'height': 75, 'sh_height': 61.098, 'hip_to_ankle': 31.167,
                 'hip_to_knee': 15.196, 'shoulder_to_wrist': 13.538,
                 'arm_len': 16.538, 'tor_len': 26.931,
                 'low_leg': 18.971, 'up_leg': 15.196},
                self.analyzer.analyze_bytes(75, file.read())
            )

    def test_get_body_dimensions_from_invalid_image(self):
        """How to tell if an image is invalid? No exception is thrown by the predictor"""
        self.assertIsNotNone(self.analyzer.get_body_dimensions(75, "resources/blank.jpeg"))

    def test_get_body_dimensions_from_image(self):
        analysis = self.analyzer.get_body_dimensions(75, "resources/image2.jpeg")
        self.assertDictAlmostEqual(
            {'height': 75, 'sh_height': 61.098, 'hip_to_ankle': 31.167,
             'hip_to_knee': 15.196, 'shoulder_to_wrist': 13.538,
             'arm_len': 16.538, 'tor_len': 26.931,
             'low_leg': 18.971, 'up_leg': 15.196},
            analysis
        )
