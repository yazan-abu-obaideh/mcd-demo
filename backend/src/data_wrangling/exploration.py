import os.path

import numpy as np
import pandas as pd
from fit_analysis.interfacepoints import interface_points


def get_good_subset():
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), "generated/bike_vector_df.csv"), index_col="Bike ID")
    points = interface_points(data.values)
    points = pd.DataFrame(points, columns=["hx", "hy", "sx", "sy", "cl"])
    return data.loc[~np.isnan(points.values).any(axis=1)]


if __name__ == "__main__":
    print(get_good_subset())
