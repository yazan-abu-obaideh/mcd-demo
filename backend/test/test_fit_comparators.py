from app_config.app_constants import APP_LOGGER
from fit_optimization.optimization_constants import KNEE_TARGET, BACK_TARGET, ARMPIT_WRIST_TARGET
from test_utils import McdDemoTestCase

IDEAL_BACK_ANGLE = (BACK_TARGET.upper_bound - BACK_TARGET.lower_bound) / 2
IDEAL_KNEE_ANGLE = (KNEE_TARGET.upper_bound - KNEE_TARGET.lower_bound) / 2
IDEAL_ARM_ANGLE = (ARMPIT_WRIST_TARGET.upper_bound - ARMPIT_WRIST_TARGET.lower_bound) / 2


def compare_aerodynamic_performance(original_bike_drag, optimized_bike_drag):
    if original_bike_drag <= optimized_bike_drag:
        APP_LOGGER.warning("Generated counterfactual with greater aerodynamic drag than original")
        return "Little change in aerodynamic drag"
    rounded_percentage = int(((abs(optimized_bike_drag - original_bike_drag) * 100) / original_bike_drag))
    return f"Offers {rounded_percentage}% reduction in aerodynamic drag"


def to_differences_dict(angles_dict):
    return {
        "Knee Extension": abs(IDEAL_KNEE_ANGLE - angles_dict["Knee Extension"]),
        "Armpit Angle": abs(IDEAL_ARM_ANGLE - angles_dict["Armpit Angle"]),
        "Back Angle": abs(IDEAL_BACK_ANGLE - angles_dict["Back Angle"])
    }


def compare_ergonomic_performance(original_angles, optimized_angles):
    original_differences = to_differences_dict(original_angles)
    optimized_differences = to_differences_dict(optimized_angles)
    max_difference = {"key": "", "value": 0}
    for key in original_differences.keys():
        diff = original_differences[key] - optimized_differences[key]
        if diff > max_difference["value"]:
            max_difference["key"] = key
            max_difference["value"] = diff
    return f"{max_difference['value']} degrees closer to desired {max_difference['key'].lower()}"


class FitComparatorsTest(McdDemoTestCase):
    def test_ergonomics_comparator(self):
        # back 25
        # arm wrist 47.5
        # knee extension 23.75
        self.assertEqual(
            "17.5 degrees closer to desired back angle",
            compare_ergonomic_performance(
                original_angles={
                    "Back Angle": 42.5,
                    "Armpit Angle": 40,
                    "Knee Extension": 40
                },
                optimized_angles={
                    "Back Angle": 25,
                    "Armpit Angle": 40,
                    "Knee Extension": 40
                }
            )
        )

    def test_aerodynamic_comparator(self):
        self.assertEqual("Offers 50% reduction in aerodynamic drag",
                         compare_aerodynamic_performance(
                             original_bike_drag=100,
                             optimized_bike_drag=50
                         ))

    def test_no_change_in_drag(self):
        self.assertEqual("Little change in aerodynamic drag",
                         compare_aerodynamic_performance(
                             original_bike_drag=50,
                             optimized_bike_drag=100
                         ))
        self.assertEqual("Little change in aerodynamic drag",
                         compare_aerodynamic_performance(
                             original_bike_drag=50,
                             optimized_bike_drag=50
                         ))
