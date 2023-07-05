import os.path
from typing import Tuple

import numpy as np
import tensorflow as tf
from scipy.stats import norm

import backend.utils as utils
from backend._validation_utils import validate
from backend.movenet import Movenet

_movenet = Movenet(os.path.join(os.path.dirname(__file__),
                                "resources/movenet_thunder.tflite"))


class PoserAnalyzer:
    def get_body_dimensions(self, camera_height, image_path):
        return _decompose_to_dictionary(_analyze(camera_height, image_path)[0])

    def get_bike_fit(self, bike: dict, body_dimensions: dict):
        prob_dists = _prob_dists(self._to_bike_vector(bike),
                                 _dict_to_body_vector(body_dimensions, 5.5, 107), 150)
        return {
            "knee": prob_dists[0][0],
            "back": prob_dists[1][0],
            "armpit_wrist": prob_dists[2][0]
        }

    def get_bikes_fit(self, bikes: np.ndarray, body_dimensions: dict) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        return _prob_dists(bikes, _dict_to_body_vector(body_dimensions, 5.5, 107), 150)

    def _to_bike_vector(self, bike: dict):
        all_keys_present = {"seat_x", "seat_y", "handle_bar_x", "handle_bar_y", "crank_length"}.issubset(
            set(bike.keys()))
        validate(all_keys_present, "Invalid bike - missing parameters")
        return np.array([
            bike["seat_x"],
            bike["seat_y"],
            bike["handle_bar_x"],
            bike["handle_bar_y"],
            bike["crank_length"]
        ]).reshape((1, 5))


def _analyze(height, imgroute):
    calc, overlayed = _calculation(height, imgroute, output_overlayed=True)
    calc = [height] + calc
    return calc, overlayed


def _prob_dists(bikes, body_vector, arm_angle, use="road"):
    """
    Computes probability of deviation from optimal for each body angle
    """
    # arm angle in radians:
    # arm_angle = float(arm_angle * (np.pi / 180))
    # min knee extension angle over sweep 0-2pi
    our_knee_angle = min(_knee_extension_angle(bikes, body_vector, np.arange(0, 30)))
    our_knee_angle = np.array([our_knee_angle])

    # back angle, armpit to elbow angle, armpit to wrist angle
    our_back_angle, our_awrist_angle = _back_armpit_angles(
        bikes, body_vector, arm_angle
    )

    k_ang_prob = _prob(
        _to_radians(_USE_DICT[use]["opt_knee_angle"][0]),
        _to_radians(_USE_DICT[use]["opt_knee_angle"][1]),
        our_knee_angle,
    )
    b_ang_prob = _prob(
        _to_radians(_USE_DICT[use]["opt_back_angle"][0]),
        _to_radians(_USE_DICT[use]["opt_back_angle"][1]),
        our_back_angle,
    )
    aw_ang_prob = _prob(
        _to_radians(_USE_DICT[use]["opt_awrist_angle"][0]),
        _to_radians(_USE_DICT[use]["opt_awrist_angle"][1]),
        our_awrist_angle,
    )
    print(f"knee extension: {_to_degrees(our_knee_angle)}")
    print(f"back angle: {_to_degrees(our_back_angle)}")
    print(f"armpit wrist: {_to_degrees(our_awrist_angle)}")

    return k_ang_prob, b_ang_prob, aw_ang_prob


def _dict_to_body_vector(user_dict, foot_len, ankle_angle):
    """
    Input: dict from decompose_to_dictionary, foot length, ankle angle degrees
    Output: body vector
    """
    return np.array(
        [user_dict["low_leg"], user_dict["up_leg"], user_dict["tor_len"], user_dict["arm_len"], foot_len,
         _to_radians(ankle_angle)]).reshape(6, 1)


def _to_radians(angle_in_degrees):
    """
    Converts degrees to radians
    """
    return float(angle_in_degrees / 180) * np.pi


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
    base["arm_len"] = base["shoulder_to_wrist"] + ankle_wrist_offset
    base["tor_len"] = base["sh_height"] - base["hip_to_ankle"] - ankle_wrist_offset
    base["low_leg"] = base["hip_to_ankle"] - base["hip_to_knee"] + ankle_wrist_offset
    base["up_leg"] = base["hip_to_knee"]

    return base


def _detect(input_tensor, inference_count=10):
    """Runs detection on an input image.

    Args:
      input_tensor: A [height, width, 3] Tensor of type tf.float32.
        Note that height and width can be anything since the image will be
        immediately resized according to the needs of the model within this
        function.
      inference_count: Number of times the model should run repeatly on the
        same input image to improve detection accuracy.

    Returns:
      A Person entity detected by the MoveNet.SinglePose.
    """

    # Detect pose using the full input image
    _movenet.detect(input_tensor.numpy(), reset_crop_region=True)

    # Repeatedly using previous detection result to identify the region of
    # interest and only croping that region to improve detection accuracy
    for _ in range(inference_count - 1):
        person = _movenet.detect(input_tensor.numpy(),
                                 reset_crop_region=False)

    return person


def _calculation(heights, imgroute, output_overlayed=True):
    z = imgroute
    image = tf.io.read_file(z)
    # height = heights
    image = tf.io.decode_jpeg(image)
    pheight = image.get_shape()[0]
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
        overlayed = utils.visualize(image.numpy(), [person])
        return pred, overlayed

    return pred


_USE_DICT = {
    "road": {
        "opt_knee_angle": (37.5, 5),
        "opt_back_angle": (45, 5),
        "opt_awrist_angle": (90, 5),
        "opt_elbow_angle": (160, 10),
        "opt_ankle_angle": (100.0, 5.0),
        "opt_hip_angle_closed": (60, 5),
    },
    "mtb": {
        "opt_knee_angle": (37.5, 2.5),
        "opt_back_angle": (45, 5),
        "opt_elbow_angle": (160, 10),
        "opt_ankle_angle": (100.0, 5.0),
        "opt_hip_angle_closed": (60, 5),
    },
    "tt": {
        "opt_knee_angle": (37.5, 2.5),
        "opt_back_angle": (45, 5),
        "opt_elbow_angle": (160, 10),
        "opt_ankle_angle": (100.0, 5.0),
        "opt_hip_angle_closed": (60, 5),
    },
    "commute": {
        "opt_knee_angle": (37.5, 2.5),
        "opt_back_angle": (45, 5),
        "opt_elbow_angle": (160, 10),
        "opt_ankle_angle": (100.0, 5.0),
        "opt_hip_angle_closed": (60, 5),
    },
}


def _prob(mean, sd, value):
    """
    Returns probability of value or larger given mean and sd
    """
    dist = abs((value - mean)) / sd
    return 1 - norm.cdf(dist, loc=0, scale=1)


def _knee_extension_angle(bike_vector, body_vector, CA, tor=False):
    """
    Input:
        bike vector, body vector, crank angle
        np array bike vector:
            [SX, SY, HX, HY, CL]^T
            (seat_x, seat_y, hbar_x, hbar_y, crank len)
        np array body vector:
            [LL, UL, TL, AL, FL, AA]
            (lowleg, upleg, torso len, arm len, foot len, ankl angle)
        CA = crank angle:
            crank angle fom horizontal in radians
        Origin is bottom bracket

    Output:
        Knee extension angle
        OR
        None if not valid coords (i.e. NaA appeared)

    """
    # decomposing body vector
    sq_body = np.square(body_vector)

    lower_leg = body_vector[0, 0]
    upper_leg = body_vector[1, 0]
    foot_length = body_vector[4, 0]
    ankle_angle = body_vector[5, 0]

    lower_leg_squared = sq_body[0, 0]
    upper_leg_squared = sq_body[1, 0]
    foot_length_squared = sq_body[4, 0]

    # decomposing bike vector

    SX = bike_vector[:, 0]
    SY = bike_vector[:, 1]
    CL = bike_vector[:, 4]

    x_1 = np.sqrt(lower_leg_squared + foot_length_squared - (2 * lower_leg * foot_length * np.cos(ankle_angle)))

    LX = CL * np.cos(CA) - SX
    LY = SY - CL * np.sin(CA)

    x_2 = np.sqrt((LX ** 2 + LY ** 2))

    alpha_1 = np.arccos((x_1 ** 2 - upper_leg_squared - x_2 ** 2) / (-2 * upper_leg * x_2))
    # if np.isnan(alpha_1):
    #     return None

    alpha_2 = np.arctan2(LY, LX) - alpha_1

    LLY = LY - upper_leg * np.sin(alpha_2)
    LLX = LX - upper_leg * np.cos(alpha_2)

    alpha_3 = np.arctan2(LLY, LLX) - alpha_2

    alpha_4 = np.arccos((foot_length_squared - lower_leg_squared - x_1 ** 2) / (-2 * lower_leg * x_1))
    # if np.isnan(alpha_4):
    #     return None

    return alpha_3 + alpha_4


def _back_armpit_angles(bikes, body_vector, elbow_angle):
    """
    Input: bike_vector, body_vector, elbow_angle
    Output: back angle, armpit to elbow angle, armpit to wrist angle in radians

     np array bike vector:
            [SX, SY, HX, HY, CL]^T
    np array body vector:
            [LL, UL, TL, AL, FL, AA]

    TL = UL
    UA = LL
    La = FL
    AA = ARM Angle
    CL = 0
    hx = -sx
    hy = -sy
    """
    elbow_angle = elbow_angle * (np.pi / 180)

    torso_length = body_vector[2, 0]
    ankle_length = float(body_vector[3, 0])

    # decomposing bike vector

    seat_x = bikes[:, 0]
    seat_y = bikes[:, 1]
    handle_bar_x = bikes[:, 2]
    handle_bar_y = bikes[:, 3]

    # BACK ANGLE
    # Calculating straightline distance between handlebars and seat
    sth_dist = ((handle_bar_y - seat_y) ** 2 + (handle_bar_x - seat_x) ** 2) ** 0.5

    # Calculating angle offset for torso angle
    sth_ang = np.arctan2((handle_bar_y - seat_y), (handle_bar_x - seat_x))

    # Uses new dist and law of cosines to find torso angle
    x_1 = (ankle_length / 2) ** 2 + (ankle_length / 2) ** 2 - 2 * (ankle_length / 2) * (ankle_length / 2) * np.cos(
        elbow_angle)
    tors_ang = np.arccos((torso_length ** 2 + sth_dist ** 2 - x_1) / (2 * torso_length * sth_dist))
    if np.isnan(tors_ang):
        return None, None

    # Adds offset to get back angle with horizontal
    back_angle = tors_ang + sth_ang

    # ARMPIT TO WRIST ANGLE
    # ARMPIT TO WRIST DIRECTLY WITH LAW OF COSINES
    armpit_to_wrist = np.arccos((torso_length ** 2 + x_1 - sth_dist ** 2) / (2 * torso_length * (x_1 ** 0.5)))

    # return angles in radians
    return back_angle, armpit_to_wrist


def _to_degrees(angle_in_radians):
    return float(angle_in_radians * (180 / np.pi))


def _all_angles(bike_vector, body_vector, arm_angle):
    """
    Input: bike, body, arm_angle in degrees
    Output: tuple (min_ke angle, back angle, awrist angle) in degrees
    """

    # min knee extension angle over sweep 0-2pi
    ke_ang = [
        item for item in (_knee_extension_angle(bike_vector, body_vector, angle * 0.2)
                          for angle in range(0, 32)) if item is not None
    ]
    if ke_ang == [] or len(ke_ang) != 32:
        ke_ang = None
    else:
        ke_ang = min(ke_ang)

    # back angle, armpit to elbow angle, armpit to wrist angle
    b_ang, aw_ang = _back_armpit_angles(bike_vector, body_vector, arm_angle)

    return [_to_degrees(ang) if ang is not None else None for ang in [ke_ang, b_ang, aw_ang]]
