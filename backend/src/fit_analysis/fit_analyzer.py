from typing import List, Dict

import numpy as np
from scipy.stats import norm

from _validation_utils import validate


class FitAnalyzer:
    def get_bike_fit(self, bike: dict, body_dimensions: dict):
        prob_dists = _prob_dists(self._to_bike_vector(bike),
                                 _dict_to_body_vector(body_dimensions, 5.5, 107), 150)
        return {
            "knee": prob_dists[0][0],
            "back": prob_dists[1][0],
            "armpit_wrist": prob_dists[2][0]
        }

    def get_bikes_fit(self, bikes: List[Dict], body_dimensions: dict) -> List[Dict]:
        bikes_fit = []
        for bike in bikes:
            try:
                fit = self.get_bike_fit(bike, body_dimensions)
            except (TypeError, ValueError):
                fit = {key: float("inf") for key in ["knee", "back", "armpit_wrist"]}
            bikes_fit.append(fit)
        return bikes_fit

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

    return k_ang_prob, b_ang_prob, aw_ang_prob


def _dict_to_body_vector(user_dict, foot_len, ankle_angle):
    """
    Input: dict from decompose_to_dictionary, foot length, ankle angle degrees
    Output: body vector
    """
    return np.array(
        [user_dict["low_leg"], user_dict["up_leg"], user_dict["tor_len"], user_dict["arm_len"], foot_len,
         _to_radians(ankle_angle)]).reshape(6, 1)


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


def _to_radians(angle_in_degrees):
    """
    Converts degrees to radians
    """
    return float(angle_in_degrees / 180) * np.pi


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
