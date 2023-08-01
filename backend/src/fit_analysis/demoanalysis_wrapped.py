import numpy as np

from fit_analysis.demoanalysis import bike_body_calculation

INFINITY = float("inf")


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
    pass
