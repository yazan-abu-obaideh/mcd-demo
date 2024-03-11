from typing import Optional

from mcd_demo.app_config.app_constants import APP_LOGGER
from mcd_demo.fit_optimization.optimization_constants import BACK_TARGET, KNEE_TARGET, ARMPIT_WRIST_TARGET

IDEAL_BACK_ANGLE = (BACK_TARGET.upper_bound - BACK_TARGET.lower_bound) / 2
IDEAL_KNEE_ANGLE = (KNEE_TARGET.upper_bound - KNEE_TARGET.lower_bound) / 2
IDEAL_ARM_ANGLE = (ARMPIT_WRIST_TARGET.upper_bound - ARMPIT_WRIST_TARGET.lower_bound) / 2


def compare_aerodynamic_performance(original, optimized):
    original_bike_drag = original["Aerodynamic Drag"]
    optimized_bike_drag = optimized["Aerodynamic Drag"]
    if original_bike_drag == float("inf") or original_bike_drag is None:
        return "Significant reduction in aerodynamic drag"

    if original_bike_drag <= optimized_bike_drag:
        APP_LOGGER.warning("Generated counterfactual with greater aerodynamic drag than original")
        return "Little or undesirable change in aerodynamic drag"
    rounded_percentage = int(((abs(optimized_bike_drag - original_bike_drag) * 100) / original_bike_drag))
    return f"Offers {rounded_percentage}% reduction in aerodynamic drag"


def compare_ergonomic_performance(original: dict, optimized: dict):
    if None in original.values() or float("inf") in original.values():
        return "Significant improvement in ergonomics"
    original_differences = _to_differences_dict(original)
    optimized_differences = _to_differences_dict(optimized)
    max_difference = _get_max_difference(optimized_differences, original_differences)
    if not max_difference:
        return "Little or undesirable change in ergonomics"
    return f"{round(max_difference['value'], 1)} degrees closer to desired {max_difference['key'].lower()}"


def _to_differences_dict(angles_dict):
    return {
        "Knee Extension": abs(IDEAL_KNEE_ANGLE - angles_dict["Knee Extension"]),
        "Armpit Angle": abs(IDEAL_ARM_ANGLE - angles_dict["Armpit Angle"]),
        "Back Angle": abs(IDEAL_BACK_ANGLE - angles_dict["Back Angle"])
    }


def _get_max_difference(optimized_differences, original_differences) -> Optional[dict]:
    max_difference = {"key": "", "value": 0}
    for key in original_differences.keys():
        diff = original_differences[key] - optimized_differences[key]
        if diff > max_difference["value"]:
            max_difference["key"] = key
            max_difference["value"] = diff
    if not max_difference["key"]:
        APP_LOGGER.warning("Generated counterfactual with worse ergonomics than original")
        return None
    return max_difference
