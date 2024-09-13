import os.path

from mcd_demo.pose_analysis.pose_image_processing import PoserAnalyzer
from test_utils import McdDemoTestCase


class ImageAnalyzerTest(McdDemoTestCase):
    def setUp(self) -> None:
        self.analyzer = PoserAnalyzer()

    def test_analyze_rider_images(self):
        rider_images = ["person1.jpg", "person2.jpg", "person3.jpg"]
        heights_mm = [1750, 1800, 1500]
        for rider_image, height_mm in zip(rider_images, heights_mm):
            path = os.path.join(os.path.dirname(__file__), "../../src/mcd_demo/resources/rider-images", rider_image)
            with open(path, "rb") as file:
                print(self.analyzer.analyze_bytes_mm(image_bytes=file.read(),
                                                     camera_height_inches=(height_mm/25.4)))

    def test_analyze_invalid_image(self):
        self.assertRaisesWithMessage(
            lambda: self.analyzer.analyze_bytes_inches(75, b"RANDOM_GARBAGE_NOT_AN_IMAGE"),
            "Invalid image"
        )

    def test_analyze_bytes(self):
        with open(self._get_path("../resources/image2.jpeg"), "rb") as file:
            self.assertDictAlmostEqual(
                {'height': 75, 'sh_height': 61.098, 'hip_to_ankle': 31.244,
                 'hip_to_knee': 14.972, 'shoulder_to_wrist': 14.639,
                 'arm_length': 17.639, 'torso_length': 26.854,
                 'lower_leg': 19.271, 'upper_leg': 14.972},
                self.analyzer.analyze_bytes_inches(75, file.read())
            )

    def test_get_body_dimensions_from_invalid_image(self):
        """How to tell if an image is invalid? No exception is thrown by the predictor"""
        self.assertIsNotNone(self.analyzer.get_body_dimensions(75, self._get_path("../resources/blank.jpeg")))

    def test_get_body_dimensions_from_image(self):
        analysis = self.analyzer.get_body_dimensions(75, self._get_path("../resources/image2.jpeg"))
        self.assertDictAlmostEqual(
            {'height': 75, 'sh_height': 61.098, 'hip_to_ankle': 31.244,
             'hip_to_knee': 14.972, 'shoulder_to_wrist': 14.639,
             'arm_length': 17.639, 'torso_length': 26.854,
             'lower_leg': 19.271, 'upper_leg': 14.972},
            analysis
        )

    def _get_path(self, rel_path):
        return os.path.join(os.path.dirname(__file__), rel_path)
