import numpy as np

from fit_analysis.demoanalysis import bike_body_calculation

INFINITY = float("inf")


def to_body_vector(body: dict):
    return np.array([
        body["low_leg"],
        body["up_leg"],
        body["tor_len"],
        body["arm_len"],
        body["foot length"],
        body["ankle angle"],
        body["shoulder_to_wrist"],
        body["height"],
    ])


def calculate_angles(bikes, body):
    return bike_body_calculation(bikes, body).fillna(INFINITY)


def calculate_angles_loss(bikes, body):
    pass
