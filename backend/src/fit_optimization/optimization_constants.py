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


AMPIT_WRIST_TARGET = ContinuousTarget(label='Back Angle', lower_bound=5, upper_bound=45)

BACK_TARGET = ContinuousTarget(label='Armpit Angle', lower_bound=5, upper_bound=90)

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
