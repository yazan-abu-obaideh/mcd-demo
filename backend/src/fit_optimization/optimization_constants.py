import pandas as pd
from decode_mcd import ContinuousTarget, DesignTargets
from pymoo.core.variable import Real

from fit_optimization.bike_dataset_builder import build_performances, build_bikes
from fit_analysis.fit_analyzer import FitAnalyzer

AMPIT_WRIST_TARGET = ContinuousTarget(label='armpit_wrist', lower_bound=0, upper_bound=0.01)

BACK_TARGET = ContinuousTarget(label='back', lower_bound=0, upper_bound=0.01)

KNEE_TARGET = ContinuousTarget(label='knee', lower_bound=0, upper_bound=0.01)
TARGETS = DesignTargets([KNEE_TARGET, BACK_TARGET, AMPIT_WRIST_TARGET, ])

FEATURES_DATATYPES = [Real(bounds=(-100, 100)) for _ in range(5)]

PERFORMANCES = pd.DataFrame.from_records(build_performances())

ANALYZER = FitAnalyzer()
all_bikes = build_bikes()
DESIGNS = pd.DataFrame.from_records(all_bikes)

SEED_BIKES_MAP = {
    "1": {
        "seat_x": -9,
        "seat_y": 27,
        "handle_bar_x": 16.5,
        "handle_bar_y": 25.5,
        "crank_length": 7,
    },
    "2": {
        "seat_x": -10,
        "seat_y": 24,
        "handle_bar_x": 13.5,
        "handle_bar_y": 29.5,
        "crank_length": 10,
    },
    "3": {
        "seat_x": -7,
        "seat_y": 30,
        "handle_bar_x": 18.5,
        "handle_bar_y": 22.5,
        "crank_length": 4,
    }
}
