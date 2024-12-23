import os.path

import cv2
import numpy as np

import mcd_demo.pose_analysis.utils as utils
from mcd_demo.exceptions import UserInputException
from mcd_demo.pose_analysis.movenet import Movenet

_movenet = Movenet(os.path.join(os.path.dirname(__file__),
                                "../resources/movenet_thunder.tflite"))


class PoserAnalyzer:
    def get_body_dimensions(self, camera_height, image_path):
        return _decompose_to_dictionary(_analyze(camera_height, image_path)[0])

    def analyze_bytes_inches(self, camera_height_inches, image_bytes):
        return _decompose_to_dictionary(_analyze_with_bytes(camera_height_inches, image_bytes)[0])

    def analyze_bytes_mm(self, camera_height_inches, image_bytes):
        inches_dict = _decompose_to_dictionary(_analyze_with_bytes(camera_height_inches, image_bytes)[0])
        return {key: value * 25.4 for key, value in inches_dict.items()}


def _analyze(height, imgroute):
    calc, overlayed = _calculation_with_img_path(height, imgroute, output_overlayed=True)
    calc = [height] + calc
    return calc, overlayed


def _analyze_with_bytes(height, img_bytes):
    calc, overlayed = _calculation_with_img_bytes(height, img_bytes, output_overlayed=True)
    calc = [height] + calc
    return calc, overlayed


def _decompose_to_dictionary(prediction_array):
    """
    Input: Array format [B: shoulder height, C: Inseam, D: Thigh, E:Arm length, F: Eye to shoulder]
    DOES NOT MODIFY INPUT
    Output: Returns dictionary "dimension name": Value in inches
      INCLUDES OFFSET BY HEIGHT
    """
    base = {
        "height": prediction_array[0],
        "sh_height": prediction_array[1],
        "hip_to_ankle": (prediction_array[2]),
        "hip_to_knee": prediction_array[3],
        "shoulder_to_wrist": prediction_array[4],
        # "sh_width": prediction_array[5],
    }
    # GETTING OFFSETS
    # Ankle height from floor to lateral malleolus and grip center to wrist are the same ratio
    ankle_wrist_offset = 0.04 * base["height"]
    base["arm_length"] = base["shoulder_to_wrist"] + ankle_wrist_offset
    base["torso_length"] = base["sh_height"] - base["hip_to_ankle"] - ankle_wrist_offset
    base["lower_leg"] = base["hip_to_ankle"] - base["hip_to_knee"] + ankle_wrist_offset
    base["upper_leg"] = base["hip_to_knee"]

    return base


def _detect(input_array: np.ndarray, inference_count=10):
    """Runs detection on an input image.

    Args:
      input_array: A [height, width, 3] array of type np.ndarray.
        Note that height and width can be anything since the image will be
        immediately resized according to the needs of the model within this
        function.
      inference_count: Number of times the model should run repeatly on the
        same input image to improve detection accuracy.

    Returns:
      A Person entity detected by the MoveNet.SinglePose.
    """

    # Detect pose using the full input image
    _movenet.detect(input_array, reset_crop_region=True)

    # Repeatedly using previous detection result to identify the region of
    # interest and only croping that region to improve detection accuracy
    for _ in range(inference_count - 1):
        person = _movenet.detect(input_array,
                                 reset_crop_region=False)

    return person


def _calculation_with_img_bytes(heights, img_bytes, output_overlayed=True):
    decoded_image = _decode_image(img_bytes)
    return _calculation(heights, decoded_image, output_overlayed)


def _decode_image(img_bytes):
    image_array = cv2.imdecode(np.frombuffer(img_bytes, dtype=np.int8), flags=cv2.IMREAD_COLOR)
    if image_array is None:
        raise UserInputException("Invalid image")
    return image_array


def _calculation_with_img_path(heights, imgroute, output_overlayed=True):
    # height = heights
    return _calculation(heights, cv2.imread(imgroute), output_overlayed)


def _calculation(heights, image: np.ndarray, output_overlayed=True):
    pheight = image.shape[0]
    person = _detect(image)
    keys = []

    # Y-axis Distortion Correction
    def ydistortionWrapper(cheight, cdistance, sheight, numpixels):
        def ydistortion(pycoord):
            a1 = np.arctan2(cheight, cdistance)
            a2 = np.arctan2((sheight - cheight), cdistance)
            p2a = numpixels / (a1 + a2)
            a3 = (pheight - pycoord) / p2a

            return cdistance * (np.tan(a1) - np.tan(a1 - a3))

        return ydistortion

    # X-axis Distortion Correction
    def xdistortionWrapper(cheight, cdistance, sheight, numpixels):
        def xdistortion(pxcoord):
            a1 = np.arctan2(cheight, cdistance)
            a2 = np.arctan2((sheight - cheight), cdistance)
            p2a = numpixels / (a1 + a2)
            # a3 = pxcoord / p2a
            return pxcoord * cdistance / p2a

        return xdistortion

    # Distance Calculation
    def distance1(x1, y1, x2, y2):
        ydis = ydistortionWrapper(62, 111, heights, pheight)
        xdis = xdistortionWrapper(62, 111, heights, pheight)
        v = np.sqrt(pow(xdis(x1) - xdis(x2), 2) + pow(ydis(y1) - ydis(y2), 2))
        return v

    # Index the points to an array
    while len(keys) == 0:
        for z1 in range(len(person.keypoints)):
            if z1 in [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]:
                keys.append(person.keypoints[z1])

    d1 = distance1(keys[6].coordinate.x, keys[6].coordinate.y, keys[8].coordinate.x, keys[8].coordinate.y)

    d2 = distance1(keys[7].coordinate.x, keys[7].coordinate.y, keys[9].coordinate.x, keys[9].coordinate.y)

    e1 = distance1(keys[1].coordinate.x, keys[1].coordinate.y, keys[3].coordinate.x,
                   keys[3].coordinate.y) + distance1(
        keys[3].coordinate.x, keys[3].coordinate.y, keys[5].coordinate.x, keys[5].coordinate.y)
    e2 = distance1(keys[0].coordinate.x, keys[0].coordinate.y, keys[2].coordinate.x,
                   keys[2].coordinate.y) + distance1(
        keys[2].coordinate.x, keys[2].coordinate.y, keys[4].coordinate.x, keys[4].coordinate.y)

    f1 = distance1(keys[0].coordinate.x, keys[0].coordinate.y, keys[1].coordinate.x, keys[1].coordinate.y)
    b1 = distance1(0, pheight, 0, keys[0].coordinate.y)
    b2 = distance1(0, pheight, 0, keys[1].coordinate.y)
    c2 = distance1(keys[9].coordinate.x, keys[9].coordinate.y, keys[11].coordinate.x, keys[11].coordinate.y) + d2
    c1 = distance1(keys[8].coordinate.x, keys[8].coordinate.y, keys[10].coordinate.x, keys[10].coordinate.y) + d1

    pred = [((b1 + b2) / 2), ((c1 + c2) / 2), ((d1 + d2) / 2), ((e1 + e2) / 2), f1]

    # Return prediction or (prediction, overlayed image) for use in analyze_and_display
    if output_overlayed:
        overlayed = utils.visualize(image, [person])
        return pred, overlayed

    return pred
