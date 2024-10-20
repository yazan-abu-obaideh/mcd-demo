from mcd_demo.fit_optimization.performance_comparators import (compare_ergonomic_performance,
                                                               compare_aerodynamic_performance)
from mcd_demo_test_case import McdDemoTestCase


class PerformanceComparatorsTest(McdDemoTestCase):
    def test_aero_handle_nan_or_infinity(self):
        self.assertEqual("Significant reduction in aerodynamic drag",
                         compare_aerodynamic_performance(
                             {"Aerodynamic Drag": float("inf")},
                             {"Aerodynamic Drag": 50}
                         ))
        self.assertEqual("Significant reduction in aerodynamic drag",
                         compare_aerodynamic_performance(
                             {"Aerodynamic Drag": None},
                             {"Aerodynamic Drag": 50}
                         ))

    def test_ergo_handle_nan_or_infinity(self):
        self.assertEqual(
            "Significant improvement in ergonomics",
            compare_ergonomic_performance(
                original=self._build_ergo_dict(None, None, None),
                optimized=self._build_ergo_dict(40, 50, 50)
            )
        )
        self.assertEqual(
            "Significant improvement in ergonomics",
            compare_ergonomic_performance(
                original=self._build_ergo_dict(float("inf"), 50, 50),
                optimized=self._build_ergo_dict(40, 50, 50)
            )
        )

    def _build_ergo_dict(self, knee_angle, armpit_angle, knee_extension):
        none_ = {
            "Back Angle": knee_angle,
            "Armpit Angle": armpit_angle,
            "Knee Extension": knee_extension
        }
        return none_

    def test_ergonomics_comparator_when_no_difference(self):
        self.assertEqual(
            "Little or undesirable change in ergonomics",
            compare_ergonomic_performance(
                original={
                    "Back Angle": 25,
                    "Armpit Angle": 40,
                    "Knee Extension": 40
                },
                optimized={
                    "Back Angle": 25,
                    "Armpit Angle": 40,
                    "Knee Extension": 40
                }
            )
        )

    def test_ergonomics_comparator(self):
        # back 25
        # arm wrist 47.5
        # knee extension 23.75
        self.assertEqual(
            "17.5 degrees closer to desired back angle",
            compare_ergonomic_performance(
                original={
                    "Back Angle": 42.54553,
                    "Armpit Angle": 40,
                    "Knee Extension": 40
                },
                optimized={
                    "Back Angle": 25,
                    "Armpit Angle": 40,
                    "Knee Extension": 40
                }
            )
        )

    def test_aerodynamic_comparator(self):
        self.assertEqual("Offers 50% reduction in aerodynamic drag",
                         compare_aerodynamic_performance(
                             original={"Aerodynamic Drag": 100},
                             optimized={"Aerodynamic Drag": 50}))

    def test_no_change_in_drag(self):
        self.assertEqual("Little or undesirable change in aerodynamic drag",
                         compare_aerodynamic_performance(original={"Aerodynamic Drag": 50},
                                                         optimized={"Aerodynamic Drag": 100}))
        self.assertEqual("Little or undesirable change in aerodynamic drag",
                         compare_aerodynamic_performance(
                             original={"Aerodynamic Drag": 50},
                             optimized={"Aerodynamic Drag": 50}
                         ))
