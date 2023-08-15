import numpy as np

from fit_analysis.demoanalysis import bike_body_calculation
from fit_analysis.vectorizedangles import prob_dists

INFINITY = float("inf")
DEFAULT_ARM_ANGLE = 150


def to_body_vector(body: dict):
    return np.array([
        body["lower_leg"],
        body["upper_leg"],
        body["torso_length"],
        body["arm_length"],
        body["foot_length"],
        body["ankle_angle"],
        body["shoulder_to_wrist"],
        body["height"],
    ])


def calculate_angles(bikes, body):
    return bike_body_calculation(bikes, body).fillna(INFINITY)


def calculate_angles_loss(bikes, body):
    br_arm_angles = np.ones((len(bikes), 1)) * DEFAULT_ARM_ANGLE
    br_angles_body = np.broadcast_to(body, (len(bikes), 8))
    return prob_dists(bikes, br_angles_body, br_arm_angles)
