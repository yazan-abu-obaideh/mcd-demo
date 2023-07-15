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
