import os.path

from pose_analysis.pose_image_processing import PoserAnalyzer
from test_utils import McdDemoTestCase


class ImageAnalyzerTest(McdDemoTestCase):
    def setUp(self) -> None:
        self.analyzer = PoserAnalyzer()

    def test_analyze_rider_images(self):
        rider_images = ["person1.jpeg", "person2.jpeg", "person3.jpeg"]
        heights_mm = [1750, 1800, 1500]
        for rider_image, height_mm in zip(rider_images, heights_mm):
            path = os.path.join(os.path.dirname(__file__), "../src/resources/rider-images", rider_image)
            with open(path, "rb") as file:
                print(self.analyzer.analyze_bytes_mm(image_bytes=file.read(),
                                                     camera_height_inches=(height_mm/25.4)))

    def test_analyze_invalid_image(self):
        self.assertRaisesWithMessage(
            lambda: self.analyzer.analyze_bytes_inches(75, b"RANDOM_GARBAGE_NOT_AN_IMAGE"),
            "Unknown image file format. One of JPEG, PNG, GIF, BMP required."
        )

    def test_analyze_bytes(self):
        with open("resources/image2.jpeg", "rb") as file:
            self.assertDictAlmostEqual(
                {'height': 75, 'sh_height': 61.098, 'hip_to_ankle': 31.167,
                 'hip_to_knee': 15.196, 'shoulder_to_wrist': 13.538,
                 'arm_length': 16.538, 'torso_length': 26.931,
                 'lower_leg': 18.971, 'upper_leg': 15.196},
                self.analyzer.analyze_bytes_inches(75, file.read())
            )

    def test_get_body_dimensions_from_invalid_image(self):
        """How to tell if an image is invalid? No exception is thrown by the predictor"""
        self.assertIsNotNone(self.analyzer.get_body_dimensions(75, "resources/blank.jpeg"))

    def test_get_body_dimensions_from_image(self):
        analysis = self.analyzer.get_body_dimensions(75, "resources/image2.jpeg")
        self.assertDictAlmostEqual(
            {'height': 75, 'sh_height': 61.098, 'hip_to_ankle': 31.167,
             'hip_to_knee': 15.196, 'shoulder_to_wrist': 13.538,
             'arm_length': 16.538, 'torso_length': 26.931,
             'lower_leg': 18.971, 'upper_leg': 15.196},
            analysis
        )
