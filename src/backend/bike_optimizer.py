import pandas as pd
from pymoo.core.variable import Real

from backend.bike_dataset_builder import build_bikes, build_performances, BODY_DIMENSIONS
from backend.pose_image_processing import PoserAnalyzer
from decode_mcd import DataPackage, DesignTargets, MultiObjectiveProblem, CounterfactualsGenerator, ContinuousTarget
import numpy as np


def predict(bikes: pd.DataFrame):
    return pd.DataFrame.from_records(PoserAnalyzer().get_bikes_fit(bikes.to_dict('records'), BODY_DIMENSIONS))


all_bikes = build_bikes()
data_package = DataPackage(
    features_dataset=pd.DataFrame.from_records(all_bikes),
    predictions_dataset=pd.DataFrame.from_records(build_performances()),
    query_x=pd.DataFrame.from_records([all_bikes[0]]),
    design_targets=DesignTargets([
        ContinuousTarget(label='knee', lower_bound=0, upper_bound=0.01),
        ContinuousTarget(label='back', lower_bound=0, upper_bound=0.01),
        ContinuousTarget(label='armpit_wrist', lower_bound=0, upper_bound=0.01),
    ]),
    datatypes=[Real(bounds=(-1000, 1000)) for _ in range(5)]
)

problem = MultiObjectiveProblem(
    data_package,
    predict,
    []
)

generator = CounterfactualsGenerator(
    problem, 1500, initialize_from_dataset=False, verbose=True
)
generator.generate(15)
print(generator.sample_with_weights(num_samples=10, cfc_weight=1, diversity_weight=1,
                                    gower_weight=1, avg_gower_weight=1, ))
