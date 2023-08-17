from typing import List

import pandas as pd
from decode_mcd import ContinuousTarget, DesignTargets
from pymoo.core.variable import Real, Choice, Variable

from fit_optimization.bike_dataset_builder import build_ergo_performances, get_bikes, build_aero_performances


def build_seed_map():
    records_list = all_bikes.to_dict("records")
    return {str(i): records_list[i] for i in range(len(records_list))}


def validate_seat_height(bike_df) -> pd.DataFrame:
    results = (bike_df["Saddle height"] - bike_df["ST Length"]) < 65
    # TODO: flipped because of how MCD handles constraints (this is not intuitive and should be fixed)
    return results.astype("int32")


BACK_TARGET = ContinuousTarget(label='Back Angle', lower_bound=5, upper_bound=45)

ARMPIT_WRIST_TARGET = ContinuousTarget(label='Armpit Angle', lower_bound=5, upper_bound=90)

KNEE_TARGET = ContinuousTarget(label='Knee Extension', lower_bound=10, upper_bound=37.5)
ERGO_TARGETS = DesignTargets([KNEE_TARGET, BACK_TARGET, ARMPIT_WRIST_TARGET, ])
AERO_TARGETS = DesignTargets(continuous_targets=[ContinuousTarget(label="Aerodynamic Drag",
                                                                  lower_bound=0,
                                                                  upper_bound=75)])

ERGO_PERFORMANCES = pd.DataFrame.from_records(build_ergo_performances())
AERO_PERFORMANCES = pd.DataFrame.from_records(build_aero_performances())

all_bikes = get_bikes()
DESIGNS = pd.DataFrame.from_records(all_bikes)
FEATURES_DATATYPES: List[Variable]
FEATURES_DATATYPES = [Real(bounds=(DESIGNS.iloc[:, _].quantile(0.05),
                                   DESIGNS.iloc[:, _].quantile(0.99))) for _ in range(13)]
FEATURES_DATATYPES.append(Choice(options=DESIGNS.iloc[:, 13].unique()))
CONSTRAINT_FUNCTIONS = [validate_seat_height]

SEED_BIKES_MAP = build_seed_map()
RIDERS_MAP = {
    "1": {'height': 1869.4399999999998, 'sh_height': 1522.4183722286996, 'hip_to_ankle': 859.4115496065015,
          'hip_to_knee': 419.2707983114694, 'shoulder_to_wrist': 520.3842323834416, 'arm_length': 595.1618323834416,
          'torso_length': 588.2292226221981, 'lower_leg': 514.9183512950322, 'upper_leg': 419.2707983114694},
    "2": {'height': 1739.8999999999999, 'sh_height': 1396.9610037614493, 'hip_to_ankle': 698.7754665416289,
          'hip_to_knee': 400.26991730501237, 'shoulder_to_wrist': 432.6829366967116, 'arm_length': 502.27893669671164,
          'torso_length': 628.5895372198203, 'lower_leg': 368.1015492366165, 'upper_leg': 400.26991730501237}
    ,
    "3": {'height': 1549.3999999999999, 'sh_height': 1276.0760388081906, 'hip_to_ankle': 726.1107548114591,
          'hip_to_knee': 370.3368640846207, 'shoulder_to_wrist': 385.2705359899362, 'arm_length': 447.24653598993626,
          'torso_length': 487.9892839967315, 'lower_leg': 417.74989072683843, 'upper_leg': 370.3368640846207}
}
