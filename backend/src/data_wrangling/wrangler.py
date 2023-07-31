import os.path

import pandas as pd


def _build_path(suffix):
    return f"{os.path.dirname(__file__)}/{suffix}"


if __name__ == "__main__":
    biked_data_path = _build_path("original_datasets/BIKED_raw.csv")
    structural_data_path = _build_path("original_datasets/all_structural_data.csv")

    biked_df = pd.read_csv(biked_data_path)
    structural_df = pd.read_csv(structural_data_path)

    structural_df.rename(columns={'Stack': 'Structural Stack'}, inplace=True)

    mergeddf = biked_df.merge(structural_df, left_on='Unnamed: 0', right_on='Unnamed: 0', how='inner')

    bike_vector_df = mergeddf[
        ['Unnamed: 0', 'DT Length', 'HT Length', 'HT Angle', 'HT LX', 'Stack', 'ST Length', 'ST Angle',
         'Seatpost LENGTH',
         'Saddle height', 'Stem length', 'Stem angle', 'Headset spacers', 'Crank length', 'Handlebar style']]

    # Constants in mm
    bike_vector_df[['DT Length', 'HT Length', 'HT LX', 'ST Length']] = bike_vector_df[
        ['DT Length', 'HT Length', 'HT LX', 'ST Length']].mul(1000)

    bike_vector_df.rename(columns={'Unnamed: 0': 'Bike ID'}, inplace=True)

    save_path = _build_path("generated/bike_vector_df.csv")
    bike_vector_df.to_csv(save_path, index=False)
