import pandas as pd
from decode_mcd.data_package import DataPackage
from decode_mcd.design_targets import *
from decode_mcd.multi_objective_problem import MultiObjectiveProblem
from decode_mcd.counterfactuals_generator import CounterfactualsGenerator


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
