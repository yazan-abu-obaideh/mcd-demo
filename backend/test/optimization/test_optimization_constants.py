import numpy as np
import pandas as pd

from mcd_demo.fit_optimization.optimization_constants import validate_seat_height
from mcd_demo_test_case import McdDemoTestCase
import numpy.testing as np_test


class OptimizationConstantsTest(McdDemoTestCase):
    def setUp(self) -> None:
        self.valid_bike = {"Crank length": 168.3832813255152,
                           "DT Length": 615.8202430783534,
                           "HT Angle": 71.19943217260575, "HT LX": 54.3,
                           "HT Length": 106.98932725554053,
                           "Handlebar style": 1,
                           "Headset spacers": 15.000009902830408,
                           "ST Angle": 70.91242684615587,
                           "ST Length": 400.3905519216799,
                           "Saddle height": 481.438978645615,
                           "Seatpost LENGTH": 264.7925283917136,
                           "Stack": 544.8214465519857,
                           "Stem angle": 10.314920419353577,
                           "Stem length": 49.943253038081394}
        self.invalid_bike = {"Crank length": 168.3832813255152,
                             "DT Length": 615.8202430783534,
                             "HT Angle": 71.19943217260575, "HT LX": 54.3,
                             "HT Length": 106.98932725554053,
                             "Handlebar style": 1,
                             "Headset spacers": 15.000009902830408,
                             "ST Angle": 70.91242684615587,
                             "ST Length": 450.3905519216799,
                             "Saddle height": 481.438978645615,
                             "Seatpost LENGTH": 264.7925283917136,
                             "Stack": 544.8214465519857,
                             "Stem angle": 10.314920419353577,
                             "Stem length": 49.943253038081394}

    def test_validate_seat_height(self):
        validation_results = validate_seat_height(
            bike_df=pd.DataFrame.from_records([self.valid_bike,
                                               self.invalid_bike]))
        self.assertEqual(validation_results.dtypes, "int32")
        np_test.assert_equal(
            validation_results.values,
            np.array([0, 1])
        )
