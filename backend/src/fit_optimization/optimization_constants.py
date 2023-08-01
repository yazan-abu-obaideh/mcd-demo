import pandas as pd
from decode_mcd import ContinuousTarget, DesignTargets
from pymoo.core.variable import Real, Choice

from fit_optimization.bike_dataset_builder import build_performances, get_bikes

AMPIT_WRIST_TARGET = ContinuousTarget(label='Back Angle', lower_bound=5, upper_bound=45)

BACK_TARGET = ContinuousTarget(label='Armpit Angle', lower_bound=5, upper_bound=90)

KNEE_TARGET = ContinuousTarget(label='Knee Extension', lower_bound=10, upper_bound=37.5)
TARGETS = DesignTargets([KNEE_TARGET, BACK_TARGET, AMPIT_WRIST_TARGET, ])

FEATURES_DATATYPES = [Real(bounds=(-1000, 1000)) for _ in range(13)] + [Choice(options=(0, 1, 2))]

PERFORMANCES = pd.DataFrame.from_records(build_performances())

all_bikes = get_bikes()
DESIGNS = pd.DataFrame.from_records(all_bikes)


def build_seed_map():
    records_list = all_bikes.to_dict("records")
    return {i: records_list[i] for i in range(len(records_list))}


SEED_BIKES_MAP = build_seed_map()
