from fit_analysis.fit_analyzer import FitAnalyzer

BODY_DIMENSIONS = {'height': 75, 'sh_height': 61.09855828510818, 'hip_to_ankle': 31.167514055725047,
                   'hip_to_knee': 15.196207871637029, 'shoulder_to_wrist': 13.538605228960089,
                   'arm_len': 16.538605228960087,
                   'tor_len': 26.931044229383136, 'low_leg': 18.971306184088018,
                   'up_leg': 15.196207871637029}


def build_bikes():
    bike = {
        "seat_x": -9,
        "seat_y": 27,
        "handle_bar_x": 16.5,
        "handle_bar_y": 25.5,
        "crank_length": 7,
    }
    second_bike = {
        "seat_x": -10,
        "seat_y": 24,
        "handle_bar_x": 13.5,
        "handle_bar_y": 29.5,
        "crank_length": 10,
    }
    third_bike = {
        "seat_x": -13,
        "seat_y": 30,
        "handle_bar_x": 18.5,
        "handle_bar_y": 22.5,
        "crank_length": 4,
    }

    return [bike, second_bike, third_bike]


def build_performances():
    return FitAnalyzer().get_bikes_fit(build_bikes(), BODY_DIMENSIONS)


if __name__ == "__main__":
    import pandas as pd

    biked_data_path = "/Users/noahwiley/Documents/Bike UROP/MeasureML-main/Frame Datasets/BIKED_raw.csv"
    structural_data_path = "/Users/noahwiley/Documents/Bike UROP/MeasureML-main/Frame Datasets/all_structural_data.csv"

    biked_df = pd.read_csv(biked_data_path)
    structural_df = pd.read_csv(structural_data_path)

    structural_df.rename(columns={'Stack': 'Structural Stack'}, inplace=True)
    print(biked_df['Stack'])
    print(structural_df['Structural Stack'])

    mergeddf = biked_df.merge(structural_df, left_on='Unnamed: 0', right_on='Unnamed: 0', how='inner')

    bike_vector_df = mergeddf[
        ['Unnamed: 0', 'DT Length', 'HT Length', 'HT Angle', 'HT LX', 'Stack', 'ST Length', 'ST Angle',
         'Seatpost LENGTH',
         'Saddle height', 'Stem length', 'Stem angle', 'Headset spacers', 'Crank length', 'Handlebar style']]

    print(bike_vector_df)

    # Constants in mm
    bike_vector_df[['DT Length', 'HT Length', 'HT LX', 'ST Length']] = bike_vector_df[
        ['DT Length', 'HT Length', 'HT LX', 'ST Length']].mul(1000)
    print(bike_vector_df)

    bike_vector_df.rename(columns={'Unnamed: 0': 'Bike ID'}, inplace=True)

    print(bike_vector_df)

    bike_vector_df.to_csv("/Users/noahwiley/Documents/Bike UROP/MeasureML-main/Frame Datasets/bike_vector_df.csv")

    bike_vector_df = pd.read_csv(
        "/Users/noahwiley/Documents/Bike UROP/MeasureML-main/Frame Datasets/bike_vector_df.csv")

    print(bike_vector_df)

    aug_aero_df = pd.read_csv(
        "/Users/noahwiley/Documents/Bike UROP/MeasureML-main/Frame Datasets/aero_data_augmented_id.csv")

    print(aug_aero_df)

    cut_aug_with_id = aug_aero_df.iloc[:4000, :]
    cut_aug_with_id.to_csv(
        "/Users/noahwiley/Documents/Bike UROP/MeasureML-main/Frame Datasets/aero_data_augmented_id_cut.csv")
    print(cut_aug_with_id)
