import os.path

import numpy as np
import pandas as pd

from mcd_demo.fit_analysis.demoanalysis import bike_body_calculation
from test_utils import McdDemoTestCase

INFINITY = float("inf")


class DemoAnalysisTest(McdDemoTestCase):
    def setUp(self) -> None:
        pass

    def test_analyze_dataset(self):
        data = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                        "../../src/mcd_demo/resources/bike_vector_df_with_id.csv")).iloc[:, 2:]
        bike_angles = bike_body_calculation(data.values, self.get_body())
        self.assertEqual(len(data), len(bike_angles))
        self.assertLess(pd.Series.sum(bike_angles.isna().any(axis=1)), 65)

    def get_body(self):
        LL = 22 * 25.4
        UL = 22 * 25.4
        TL = 21 * 25.4
        AL = 24 * 25.4
        FL = 5.5 * 25.4
        AA = 105
        SW = 12 * 25.4
        HT = 71 * 25.4
        return np.array([[LL, UL, TL, AL, FL, AA, SW, HT]])
