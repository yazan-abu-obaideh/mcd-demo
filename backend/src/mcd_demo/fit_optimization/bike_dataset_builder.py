import os.path

import numpy as np
import pandas as pd

from mcd_demo.fit_analysis.demoanalysis_wrapped import calculate_angles, calculate_drag


def get_bikes():
    csv_path = os.path.join(os.path.dirname(__file__), "../resources/bike_vector_df_with_id.csv")
    return pd.read_csv(csv_path).drop(columns=["Bike ID"]).set_index("Unnamed: 0")


def build_ergo_performances():
    body = _get_body()
    return calculate_angles(get_bikes().values, body)


def _get_body():
    ll = 22 * 25.4
    ul = 22 * 25.4
    tl = 21 * 25.4
    al = 24 * 25.4
    fl = 5.5 * 25.4
    aa = 105
    sw = 12 * 25.4
    ht = 71 * 25.4
    body = np.array([[ll, ul, tl, al, fl, aa, sw, ht]])
    return body


def build_aero_performances():
    return calculate_drag(get_bikes().values, _get_body())
