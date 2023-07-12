import pandas as pd
from backend.bike_dataset_builder import build_bikes, build_performances
from decode_mcd import DataPackage, DesignTargets, MultiObjectiveProblem, CounterfactualsGenerator
import numpy as np


def predict(bikes: pd.DataFrame):
    return np.array([])


data_package = DataPackage(
    features_dataset=np.ndarray([[]]),
    predictions_dataset=np.ndarray([[]]),
    query_x=np.ndarray([[]]),
    design_targets=DesignTargets(),
    datatypes=[]
)

problem = MultiObjectiveProblem(
    data_package,
    predict,
    []
)

generator = CounterfactualsGenerator(
    problem, 500, initialize_from_dataset=False, verbose=True
)
