import os.path
from typing import Union, List

import numpy as np
import pandas as pd
from pymoo.core.variable import Variable

from mcd_demo.app_config.app_parameters import SAMPLE_CLIPS_SUBSET
from mcd_demo.bike_embedding.embedding_comparator import get_cosine_distance
from mcd_demo.bike_embedding.embedding_predictor import EmbeddingPredictor
from mcd_demo.datasets.clips.datatypes_mapper import map_column
from mcd_demo.resource_utils import resource_path

PREDICTOR = EmbeddingPredictor()

CONSTANT_COLUMNS = ['Wall thickness Bottom Bracket', 'Wall thickness Top tube',
                    'Wall thickness Head tube', 'Wall thickness Down tube',
                    'Wall thickness Chain stay',
                    'Wall thickness Seat stay',
                    'Wall thickness Seat tube']


def get_features() -> pd.DataFrame:
    return pd.read_csv(resource_path(os.path.join("clips", "clip_sBIKED_processed.csv")), index_col=0)


FEATURES: pd.DataFrame
if SAMPLE_CLIPS_SUBSET:
    FEATURES = get_features().sample(500)
else:
    FEATURES = get_features()
TRIMMED_FEATURES = FEATURES.drop(columns=CONSTANT_COLUMNS)


def predict_from_partial_dataframe(designs, target_embedding) -> np.ndarray:
    full_designs_df = to_full_clips_dataframe(designs)
    return get_cosine_distance(PREDICTOR.predict(full_designs_df), target_embedding)


def to_full_clips_dataframe(designs: Union[np.ndarray, pd.DataFrame]) -> pd.DataFrame:
    designs_copy = pd.DataFrame(designs, columns=TRIMMED_FEATURES.columns)
    designs_copy = designs_copy.fillna(TRIMMED_FEATURES.mean())
    for column in CONSTANT_COLUMNS:
        designs_copy[column] = FEATURES[column].mean()
    return designs_copy


def map_datatypes() -> List[Variable]:
    datatypes = []
    for column_name in list(FEATURES.columns):
        if column_name not in CONSTANT_COLUMNS:
            datatypes.append(map_column(FEATURES[column_name]))
    return datatypes
