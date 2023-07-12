from backend.fit_analysis.fit_analyzer import FitAnalyzer
from backend.pose_analysis.pose_image_processing import PoserAnalyzer

BODY_DIMENSIONS = {'height': 75, 'sh_height': 61.09855828510818, 'hip_to_ankle': 31.167514055725047,
                   'hip_to_knee': 15.196207871637029, 'shoulder_to_wrist': 13.538605228960089,
                   'arm_len': 16.538605228960087,
                   'tor_len': 26.931044229383136, 'low_leg': 18.971306184088018,
                   'up_leg': 15.196207871637029}


def build_bikes():
    bike = {
        "seat_x": -9,
        "seat_y": 27,
        "handle_bar_x": 16.5,
        "handle_bar_y": 25.5,
        "crank_length": 7,
    }
    second_bike = {
        "seat_x": -10,
        "seat_y": 24,
        "handle_bar_x": 13.5,
        "handle_bar_y": 29.5,
        "crank_length": 10,
    }
    third_bike = {
        "seat_x": -13,
        "seat_y": 30,
        "handle_bar_x": 18.5,
        "handle_bar_y": 22.5,
        "crank_length": 4,
    }

    return [bike, second_bike, third_bike]


def build_performances():
    return FitAnalyzer().get_bikes_fit(build_bikes(), BODY_DIMENSIONS)
