import time
from abc import abstractmethod
from typing import Callable

from decode_mcd import DataPackage, MultiObjectiveProblem, CounterfactualsGenerator

from mcd_demo._validation_utils import validate
from mcd_demo.app_config.optimization_parameters import OPTIMIZER_GENERATIONS, OPTIMIZER_POPULATION
from mcd_demo.exceptions import UserInputException
from mcd_demo.fit_analysis.demoanalysis_wrapped import calculate_angles, to_body_vector, calculate_drag
from mcd_demo.fit_optimization.const_maps import RIDERS_MAP
from mcd_demo.fit_optimization.optimization_constants import *
from mcd_demo.fit_optimization.performance_comparators import compare_ergonomic_performance, \
    compare_aerodynamic_performance
from mcd_demo.pose_analysis.pose_image_processing import PoserAnalyzer


class LoggingGenerator(CounterfactualsGenerator):
    """Note that the logs_list is never 'cleaned'... Instances of LoggingGenerator
    are single-use objects and should be garbage-collected ASAP"""

    def __init__(self, problem: MultiObjectiveProblem, pop_size: int, initialize_from_dataset):
        super().__init__(problem, pop_size, initialize_from_dataset=initialize_from_dataset, verbose=True)
        self.logs_list = []

    def _log(self, log_message):
        self.logs_list.append(log_message)
        super()._log(log_message)

    def _verbose_log(self, log_message):
        self.logs_list.append(log_message)
        super()._verbose_log(log_message)


class BikeOptimizer:
    def __init__(self, image_analysis_service):
        self.image_analysis_service = image_analysis_service

    def optimize_text_prompt(self, text_prompt: str):
        return {"bikes": [{
            "bike": {
                "Crank length": 165.71345389760594,
                "DT Length": 658.7930141487176,
                "HT Angle": 68.85389727412779,
                "HT LX": 42.27049259201229,
                "HT Length": 116.80374554968037,
                "Handlebar style": 1,
                "Headset spacers": 20.063040156415063,
                "ST Angle": 72.9685740048344,
                "ST Length": 291.5123690271636,
                "Saddle height": 426.59492333782987,
                "Seatpost LENGTH": 224.3102305896304,
                "Stack": 565.6,
                "Stem angle": -2.4640376023750505,
                "Stem length": 109.90679921396946
            },
            "bikePerformance": "Significant improvement in ergonomics"
        }],
            "logs": ["1", "2", "3"]}

    @abstractmethod
    def optimize_for_dimensions(self, seed_bike_id: str, rider_dimensions_inches: dict):
        pass

    @abstractmethod
    def optimize_for_seeds(self, seed_bike_id: str, rider_id: str):
        pass

    @abstractmethod
    def optimize_for_image(self,
                           seed_bike_id: str,
                           image: bytes,
                           rider_height: float):
        pass

    def _to_full_dimensions_mm(self, rider_dimensions_inches: dict):
        mm_dimensions = {key: value * 25.4 for key, value in rider_dimensions_inches.items()}
        mm_dimensions["foot_length"] = 5.5 * 25.4
        mm_dimensions["ankle_angle"] = 100
        return mm_dimensions

    def _optimize(self, generator: LoggingGenerator,
                  prediction_function: Callable[[pd.DataFrame], pd.DataFrame],
                  performance_comparator: Callable[[dict], str]):
        # noinspection PyTypeChecker

        # noinspection PyTypeChecker
        generator.generate(OPTIMIZER_GENERATIONS)

        sampling_start = time.time()
        bikes = generator.sample_with_weights(num_samples=5, cfc_weight=1, diversity_weight=1, gower_weight=1,
                                              avg_gower_weight=1, include_dataset=False)
        print(f"sampling took {time.time() - sampling_start}")
        optimized_records = bikes.to_dict("records")
        performances = prediction_function(bikes).to_dict("records")
        return {"bikes": self._to_list_of_pairs(optimized_records,
                                                performances,
                                                performance_comparator),
                "logs": generator.logs_list}

    def _to_list_of_pairs(self, optimized_records, performances, performance_comparator: Callable[[dict], str]):
        _to_list_of_pairs = [{"bike": record, "bikePerformance": performance_comparator(performance)}
                             for (record, performance) in
                             zip(optimized_records, performances)]
        return _to_list_of_pairs

    def _get_initialize_from_dataset(self, rider_id):
        if str(rider_id) == "3":
            return True
        return False

    def _get_full_body_dimensions(self, rider_id):
        body_dimensions = self._get_body_dimensions_by_id(rider_id)
        body_dimensions["foot_length"] = 5.5 * 25.4
        body_dimensions["ankle_angle"] = 100
        return body_dimensions

    def _build_comparator(self, comparator, original_bike, prediction_function):
        return lambda optimized_performance: comparator(
            original=prediction_function(pd.DataFrame.from_records([original_bike])).to_dict("records")[0],
            optimized=optimized_performance
        )

    def _get_dimensions_from_image(self, image, rider_height):
        body_dimensions = self.image_analysis_service.analyze_bytes_mm(rider_height, image)
        body_dimensions["foot_length"] = 5.5 * 25.4
        body_dimensions["ankle_angle"] = 100
        return body_dimensions

    def _get_bike_by_id(self, seed_bike_id):
        seed_bike = TEMP_SEED_BIKES_MAP.get(str(seed_bike_id))
        validate(seed_bike is not None, f"Invalid seed bike ID [{seed_bike_id}]")
        return seed_bike

    def _get_body_dimensions_by_id(self, rider_id):
        rider = RIDERS_MAP.get(str(rider_id))
        if rider is None:
            raise UserInputException(f"Invalid rider ID [{rider_id}]")
        return rider


class ErgonomicsOptimizer(BikeOptimizer):
    def __init__(self, image_analysis_service: PoserAnalyzer):
        super().__init__(image_analysis_service)
        self.image_analysis_service = image_analysis_service

    def optimize_for_dimensions(self, seed_bike_id, rider_dimensions_inches):
        return self._optimize_ergonomics(seed_bike_id, self._to_full_dimensions_mm(rider_dimensions_inches))

    def optimize_for_seeds(self, seed_bike_id, rider_id):
        dimensions = self._get_full_body_dimensions(rider_id)
        return self._optimize_ergonomics(seed_bike_id, dimensions, self._get_initialize_from_dataset(rider_id))

    def optimize_for_image(self,
                           seed_bike_id: str,
                           image: bytes,
                           rider_height: float):
        return self._optimize_ergonomics(seed_bike_id,
                                         self._get_dimensions_from_image(image,
                                                                         rider_height))

    def _build_ergo_generator(self, predict, seed_bike, initialize_from_dataset):
        data_package = DataPackage(
            features_dataset=DESIGNS,
            predictions_dataset=ERGO_PERFORMANCES,
            query_x=pd.DataFrame.from_records([seed_bike]),
            design_targets=ERGO_TARGETS,
            datatypes=FEATURES_DATATYPES
        )
        problem = MultiObjectiveProblem(data_package, predict, CONSTRAINT_FUNCTIONS)
        generator = LoggingGenerator(problem, OPTIMIZER_POPULATION, initialize_from_dataset)
        return generator

    def _optimize_ergonomics(self, seed_bike_id, body_dimensions, initialize_from_dataset=False):
        original_bike = self._get_bike_by_id(seed_bike_id)

        def ergo_prediction_function(bikes):
            return self._predict_ergonomics(bikes, body_dimensions)

        generator = self._build_ergo_generator(
            ergo_prediction_function,
            original_bike,
            initialize_from_dataset
        )
        return self._optimize(generator, ergo_prediction_function,
                              self._build_comparator(
                                  comparator=compare_ergonomic_performance,
                                  original_bike=original_bike,
                                  prediction_function=ergo_prediction_function))

    def _predict_ergonomics(self, bikes, user_dimensions):
        start = time.time()
        response = calculate_angles(bikes.values, to_body_vector(user_dimensions))
        print(f"Took {time.time() - start}")
        return response


class AerodynamicsOptimizer(BikeOptimizer):
    def __init__(self, image_analysis_service: PoserAnalyzer):
        super().__init__(image_analysis_service)

    def optimize_for_dimensions(self, seed_bike_id, rider_dimensions_inches):
        return self._optimize_aerodynamics(seed_bike_id, self._to_full_dimensions_mm(rider_dimensions_inches))

    def optimize_for_seeds(self, seed_bike_id, rider_id):
        return self._optimize_aerodynamics(seed_bike_id,
                                           self._get_full_body_dimensions(rider_id),
                                           self._get_initialize_from_dataset(rider_id))

    def optimize_for_image(self,
                           seed_bike_id: str,
                           image: bytes,
                           rider_height: float):
        return self._optimize_aerodynamics(
            seed_bike_id,
            self._get_dimensions_from_image(
                image,
                rider_height
            )
        )

    def _optimize_aerodynamics(self, seed_bike_id, user_dimensions, initialize_from_dataset=False):
        original_bike = self._get_bike_by_id(seed_bike_id)

        def aero_prediction_function(bikes):
            return self._predict_aerodynamics(bikes, user_dimensions)

        generator = self._build_aero_generator(
            aero_prediction_function,
            original_bike,
            initialize_from_dataset
        )
        return self._optimize(generator, aero_prediction_function,
                              self._build_comparator(compare_aerodynamic_performance,
                                                     original_bike,
                                                     aero_prediction_function
                                                     ))

    def _predict_aerodynamics(self, bikes, user_dimensions):
        start = time.time()
        response = calculate_drag(bikes.values, to_body_vector(user_dimensions))
        print(f"Took {time.time() - start}")
        return response

    def _build_aero_generator(self, predict, seed_bike, initialize_from_dataset):
        data_package = DataPackage(
            features_dataset=DESIGNS,
            predictions_dataset=AERO_PERFORMANCES,
            query_x=pd.DataFrame.from_records([seed_bike]),
            design_targets=AERO_TARGETS,
            datatypes=FEATURES_DATATYPES,
            bonus_objectives=["Aerodynamic Drag"]
        )
        problem = MultiObjectiveProblem(data_package, predict, CONSTRAINT_FUNCTIONS)
        generator = LoggingGenerator(problem, OPTIMIZER_POPULATION, initialize_from_dataset)
        return generator
