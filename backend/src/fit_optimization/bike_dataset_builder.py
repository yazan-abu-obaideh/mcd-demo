import os.path

import numpy as np
import pandas as pd

from fit_analysis.demoanalysis_wrapped import calculate_angles, calculate_drag

BODY_DIMENSIONS = {'height': 75, 'sh_height': 61.09855828510818, 'hip_to_ankle': 31.167514055725047,
                   'hip_to_knee': 15.196207871637029, 'shoulder_to_wrist': 13.538605228960089,
                   'arm_len': 16.538605228960087,
                   'tor_len': 26.931044229383136, 'low_leg': 18.971306184088018,
                   'up_leg': 15.196207871637029}


def get_bikes():
    csv_path = os.path.join(os.path.dirname(__file__), "../resources/bike_vector_df_with_id.csv")
    return pd.read_csv(csv_path).drop(columns=["Bike ID"]).set_index("Unnamed: 0")


def build_ergo_performances():
    body = _get_body()
    return calculate_angles(get_bikes().values, body)


def _get_body():
    LL = 22 * 25.4
    UL = 22 * 25.4
    TL = 21 * 25.4
    AL = 24 * 25.4
    FL = 5.5 * 25.4
    AA = 105
    SW = 12 * 25.4
    HT = 71 * 25.4
    body = np.array([[LL, UL, TL, AL, FL, AA, SW, HT]])
    return body


def build_aero_performances():
    return calculate_drag(get_bikes().values, _get_body())
