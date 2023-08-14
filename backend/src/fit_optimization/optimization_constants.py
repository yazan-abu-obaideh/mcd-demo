from typing import List

import pandas as pd
from decode_mcd import ContinuousTarget, DesignTargets
from pymoo.core.variable import Real, Choice, Variable

from fit_optimization.bike_dataset_builder import build_performances, get_bikes


def build_seed_map():
    records_list = all_bikes.to_dict("records")
    return {str(i): records_list[i] for i in range(len(records_list))}


def validate_seat_height(bike_df) -> pd.DataFrame:
    results = (bike_df["Saddle height"] - bike_df["ST Length"]) < 65
    # TODO: flipped because of how MCD handles constraints (this is not intuitive and should be fixed)
    return results.astype("int32")


BACK_TARGET = ContinuousTarget(label='Back Angle', lower_bound=5, upper_bound=45)

AMPIT_WRIST_TARGET = ContinuousTarget(label='Armpit Angle', lower_bound=5, upper_bound=90)

KNEE_TARGET = ContinuousTarget(label='Knee Extension', lower_bound=10, upper_bound=37.5)
TARGETS = DesignTargets([KNEE_TARGET, BACK_TARGET, AMPIT_WRIST_TARGET, ])

PERFORMANCES = pd.DataFrame.from_records(build_performances())

all_bikes = get_bikes()
DESIGNS = pd.DataFrame.from_records(all_bikes)
FEATURES_DATATYPES: List[Variable]
FEATURES_DATATYPES = [Real(bounds=(DESIGNS.iloc[:, _].quantile(0.05),
                                   DESIGNS.iloc[:, _].quantile(0.99))) for _ in range(13)]
FEATURES_DATATYPES.append(Choice(options=DESIGNS.iloc[:, 13].unique()))
CONSTRAINT_FUNCTIONS = [validate_seat_height]

SEED_BIKES_MAP = build_seed_map()
RIDERS_MAP = {
    "1": {'height': 1750.0000000000002, 'sh_height': 1429.803836126445, 'hip_to_ankle': 831.1594731503548,
          'hip_to_knee': 437.6634157246667, 'shoulder_to_wrist': 444.7186030888706, 'arm_length': 514.7186030888705,
          'torso_length': 528.6443629760904, 'lower_leg': 463.49605742568804, 'upper_leg': 437.6634157246667},
    "2": {'height': 1800.0, 'sh_height': 1375.997605076646, 'hip_to_ankle': 744.2386180274794,
          'hip_to_knee': 390.90445268758515, 'shoulder_to_wrist': 334.9436431357713, 'arm_length': 406.9436431357713,
          'torso_length': 559.7589870491665, 'lower_leg': 425.33416533989424, 'upper_leg': 390.90445268758515},
    "3": {'height': 1500.0, 'sh_height': 1074.8980294407877, 'hip_to_ankle': 396.87407246102737,
          'hip_to_knee': 187.19943177185922, 'shoulder_to_wrist': 244.36887227919578, 'arm_length': 304.3688722791957,
          'torso_length': 618.0239569797604, 'lower_leg': 269.67464068916814, 'upper_leg': 187.19943177185922}

}
