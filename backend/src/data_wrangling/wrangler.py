import pandas as pd
import numpy as np

biked_data_path = "BIKED_raw.csv"
structural_data_path = "all_structural_data.csv"

biked_df = pd.read_csv(biked_data_path)
structural_df = pd.read_csv(structural_data_path)

structural_df.rename(columns={'Stack': 'Structural Stack'}, inplace=True)

mergeddf = biked_df.merge(structural_df, left_on='Unnamed: 0', right_on='Unnamed: 0', how='inner')

bike_vector_df = mergeddf[
    ['Unnamed: 0', 'DT Length', 'HT Length', 'HT Angle', 'HT LX', 'Stack', 'ST Length', 'ST Angle', 'Seatpost LENGTH',
     'Saddle height', 'Stem length', 'Stem angle', 'Headset spacers', 'Crank length', 'Handlebar style']]


# Constants in mm
bike_vector_df[['DT Length', 'HT Length', 'HT LX', 'ST Length']] = bike_vector_df[
    ['DT Length', 'HT Length', 'HT LX', 'ST Length']].mul(1000)

bike_vector_df.rename(columns={'Unnamed: 0': 'Bike ID'}, inplace=True)


bike_vector_df.to_csv("/Users/noahwiley/Documents/Bike UROP/MeasureML-main/Frame Datasets/bike_vector_df.csv")

bike_vector_df = pd.read_csv("/Users/noahwiley/Documents/Bike UROP/MeasureML-main/Frame Datasets/bike_vector_df.csv")

