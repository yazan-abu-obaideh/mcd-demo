import os.path

import pandas as pd
from pymoo.core.variable import Real, Integer, Choice

from mcd_demo.resource_utils import resource_path

_NUMERIC_MAPPINGS = {
    "float64": lambda lower_bound, upper_bound: Real(bounds=(lower_bound, upper_bound)),
    "int64": lambda lower_bound, upper_bound: Integer(bounds=(lower_bound, upper_bound)),
}

_NAME_TO_TYPE = pd.read_csv(resource_path(os.path.join("clips", "clip_sBIKED_processed_datatypes.csv")),
                            index_col=0)

ONE_HOT_ENCODED_CLIPS_COLUMNS = ['MATERIAL', 'Dropout spacing style',
                                 'Head tube type', 'BELTorCHAIN',
                                 'bottle SEATTUBE0 show', 'RIM_STYLE front',
                                 'RIM_STYLE rear', 'Handlebar style',
                                 'bottle DOWNTUBE0 show', 'Stem kind',
                                 'Fork type', 'Top tube type']


def map_column(column: pd.Series):
    column_datatype = _NAME_TO_TYPE.loc[column.name].values[0]
    if column_datatype == "bool":
        print(f"Mapped {column.name} to Choice")
        return Choice(options=(0, 1))
    lower_bound = column.quantile(0.02)
    upper_bound = column.quantile(0.98)
    if lower_bound == upper_bound:
        print(f"Warning: {column.name} has a range of 0")
    print(f"Mapped {column.name} to numeric with range {(lower_bound, upper_bound)}")
    return _NUMERIC_MAPPINGS[column_datatype](lower_bound, upper_bound)
