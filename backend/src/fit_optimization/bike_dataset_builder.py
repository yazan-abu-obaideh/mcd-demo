from fit_analysis.fit_analyzer import FitAnalyzer
import numpy as np

BODY_DIMENSIONS = {'height': 75, 'sh_height': 61.09855828510818, 'hip_to_ankle': 31.167514055725047,
                   'hip_to_knee': 15.196207871637029, 'shoulder_to_wrist': 13.538605228960089,
                   'arm_len': 16.538605228960087,
                   'tor_len': 26.931044229383136, 'low_leg': 18.971306184088018,
                   'up_leg': 15.196207871637029}


# def interface_points(bike, hbar_type="drops"):
#     """
#     Output:
#         Tuple of interface points: ((hand x, hand y), (seatx, seaty), (crank length))
#     """
#     # Constants in mm
#     BEARING_STACK = 10  # Stack height of bearing
#     STEM_E = 40  # Stem extension
#
#     def top_headtube():
#         # Headtube functional length
#         newHTL = bike['HT Length'] - bike['HT LX']
#
#         # Stack height - headtube length * sin(headtube angle)
#         # TODO: stack height??
#         DTy = bike['Stack Height'] - newHTL * np.sin(bike['HT Angle'])
#
#         # Pythagorean theorem
#         DTx = np.sqrt(bike['DT Length'] ** 2 - DTy ** 2)
#
#         # Offset from ht and dt intersection
#         HTx_offset = newHTL * np.cos(bike['HT Angle'])
#
#         # Subtract offset (top of headtube is beind intersection)
#         HTx = DTx - HTx_offset
#
#         # HTy and HTx matrix
#         # [[HTx1, HTy1]
#         # [HTx2, HTy2]...]
#         # np.hstack((HTx, bike[:,4]))
#         # 2 vectors HTx and HTy
#         return HTx, bike['Stack Height']
#
#     def seat_check_and_pos():
#         # TODO: saddle height?
#         Sx = bike['Saddle Height'] * np.cos(bike['ST Angle'])
#         Sy = bike['Saddle Height'] * np.sin(bike['ST Angle'])
#         # 2 Vectors Sx and Sy
#         return Sx, Sy
#
#     def hand_pos(headx, heady):
#         # Total extension of stem above headtube
#         UXL = BEARING_STACK + bike['Spacer Amt'] + STEM_E / 2
#
#         # X and Y of Middle of Stem clamp
#         SCx = headx - (UXL * np.cos(bike['HT Angle']))
#         SCy = heady + (UXL * np.sin(bike['HT Angle']))
#
#         # X and Y of handlebar Clamp
#         HBx = SCx + bike['Stem Len'] * np.cos((np.pi / 2) - bike['HT Angle'] - bike['Stem Angle'])
#         HBy = SCy + bike['Stem Len'] * np.sin((np.pi / 2) - bike['HT Angle'] - bike['Stem Angle'])
#         print("HBX, HBY", HBx, HBy)
#
#         # x and y of hand
#         match hbar_type:
#             case "drops":
#                 Hx = HBx + 100
#                 Hy = HBy + 20
#             case "mtb":
#                 Hx = HBx - 20
#                 Hy = HBy + 0
#             case "bullhorn":
#                 Hx = HBx + 100
#                 Hy = HBy + 10
#             case _:
#                 raise ValueError(f"Invalid handlebar type: {hbar_type}, must be 'drops', 'mtb', or 'bullhorn'")
#         # 2 vectors Handx and Handy
#         return Hx, Hy
#
#     # Calculate interface points
#     htx, hty = top_headtube()  # Top of headtube
#     sx, sy = seat_check_and_pos()  # Seat position uses saddle height
#     hx, hy = hand_pos(htx, hty)  # Hand position uses top of headtube position
#
#     # Reshaping to 2D arrays
#     reshaped = []
#     for vec in [hx, hy, sx, sy, bike['Crank Length']]:
#         reshaped.append(vec.reshape((len(vec), 1)))
#     print("reshaped", reshaped)
#
#     # n x 5 array: hx, hy, sx, sy, crank length
#
#     return np.hstack(reshaped)


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
