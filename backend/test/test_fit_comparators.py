from fit_optimization.performance_comparators import compare_ergonomic_performance, compare_aerodynamic_performance
from test_utils import McdDemoTestCase


class FitComparatorsTest(McdDemoTestCase):
    def test_ergonomics_comparator_when_no_difference(self):
        self.assertEqual(
            "Little change in ergonomics",
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
        self.assertEqual("Little change in aerodynamic drag",
                         compare_aerodynamic_performance(original={"Aerodynamic Drag": 50},
                                                         optimized={"Aerodynamic Drag": 100}))
        self.assertEqual("Little change in aerodynamic drag",
                         compare_aerodynamic_performance(
                             original={"Aerodynamic Drag": 50},
                             optimized={"Aerodynamic Drag": 50}
                         ))
