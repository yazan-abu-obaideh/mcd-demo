import time
from typing import Callable

from decode_mcd import DataPackage, MultiObjectiveProblem, CounterfactualsGenerator

from _validation_utils import validate
from app_config.optimization_parameters import OPTIMIZER_GENERATIONS, OPTIMIZER_POPULATION
from exceptions import UserInputException
from fit_analysis.demoanalysis_wrapped import calculate_angles, to_body_vector, calculate_drag
from fit_optimization.optimization_constants import *
from pose_analysis.pose_image_processing import PoserAnalyzer


class LoggingGenerator(CounterfactualsGenerator):
    """Note that the logs_list is never 'cleaned'... Instances of LoggingGenerator
    are single-use objects and should be garbage-collected ASAP"""

    def __init__(self, problem: MultiObjectiveProblem, pop_size: int):
        super().__init__(problem, pop_size, initialize_from_dataset=False, verbose=True)
        self.logs_list = []

    def _log(self, log_message):
        self.logs_list.append(log_message)
        super()._log(log_message)

    def _verbose_log(self, log_message):
        self.logs_list.append(log_message)
        super()._verbose_log(log_message)


class BikeOptimizer:
    def __init__(self, image_analysis_service: PoserAnalyzer):
        self.image_analysis_service = image_analysis_service

    def optimize_aerodynamics_for_seeds(self, seed_bike_id, rider_id):
        return self._optimize_aerodynamics(seed_bike_id,
                                           self._get_full_body_dimensions(rider_id))

    def optimize_aerodynamics_for_custom_rider(self,
                                               seed_bike_id: str,
                                               image: bytes,
                                               person_height: float,
                                               camera_height: float):
        return self._optimize_aerodynamics(
            seed_bike_id,
            self._get_dimensions_from_image(
                image,
                camera_height,
                person_height
            )
        )

    def optimize_ergonomics_for_seeds(self, seed_bike_id, rider_id):
        dimensions = self._get_full_body_dimensions(rider_id)
        return self._optimize_ergonomics(seed_bike_id, dimensions)

    def optimize_ergonomics_for_custom_rider(self,
                                             seed_bike_id: str,
                                             image: bytes,
                                             person_height: float,
                                             camera_height: float):
        return self._optimize_ergonomics(seed_bike_id,
                                         self._get_dimensions_from_image(image,
                                                                         camera_height,
                                                                         person_height))

    def _get_full_body_dimensions(self, rider_id):
        body_dimensions = self._get_body_dimensions_by_id(rider_id)
        body_dimensions["foot_length"] = 5.5 * 25.4
        body_dimensions["ankle_angle"] = 24 * 25.4
        return body_dimensions

    def _get_dimensions_from_image(self, image, camera_height, person_height):
        body_dimensions = self.image_analysis_service.analyze_bytes_mm(camera_height, image)
        print(f"{person_height=}")
        body_dimensions["foot_length"] = 5.5 * 25.4
        body_dimensions["ankle_angle"] = 24 * 25.4
        return body_dimensions

    def _optimize_aerodynamics(self, seed_bike_id, user_dimensions):
        def aero_prediction_function(bikes):
            return self._predict_aerodynamics(bikes, user_dimensions)

        generator = self._build_aero_generator(
            aero_prediction_function,
            self._get_bike_by_id(seed_bike_id)
        )
        return self._optimize(generator, aero_prediction_function)

    def _optimize_ergonomics(self, seed_bike_id, body_dimensions):
        def ergo_prediction_function(bikes):
            return self._predict_ergonomics(bikes, body_dimensions)

        generator = self._build_ergo_generator(
            ergo_prediction_function,
            self._get_bike_by_id(seed_bike_id)
        )
        return self._optimize(generator, ergo_prediction_function)

    def _predict_ergonomics(self, bikes, user_dimensions):
        start = time.time()
        response = calculate_angles(bikes.values, to_body_vector(user_dimensions))
        print(f"Took {time.time() - start}")
        return response

    def _predict_aerodynamics(self, bikes, user_dimensions):
        start = time.time()
        response = calculate_drag(bikes.values, to_body_vector(user_dimensions))
        print(f"Took {time.time() - start}")
        return response

    def _optimize(self, generator: LoggingGenerator,
                  prediction_function: Callable[[pd.DataFrame], pd.DataFrame]):
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
                                                performances),
                "logs": generator.logs_list}

    def _to_list_of_pairs(self, optimized_records, performances):
        _to_list_of_pairs = [{"bike": record, "bikePerformance": performance} for (record, performance) in
                             zip(optimized_records, performances)]
        return _to_list_of_pairs

    def _build_ergo_generator(self, predict, seed_bike):
        data_package = DataPackage(
            features_dataset=DESIGNS,
            predictions_dataset=ERGO_PERFORMANCES,
            query_x=pd.DataFrame.from_records([seed_bike]),
            design_targets=ERGO_TARGETS,
            datatypes=FEATURES_DATATYPES
        )
        problem = MultiObjectiveProblem(data_package, predict, CONSTRAINT_FUNCTIONS)
        generator = LoggingGenerator(problem, OPTIMIZER_POPULATION)
        return generator

    def _build_aero_generator(self, predict, seed_bike):
        data_package = DataPackage(
            features_dataset=DESIGNS,
            predictions_dataset=AERO_PERFORMANCES,
            query_x=pd.DataFrame.from_records([seed_bike]),
            design_targets=AERO_TARGETS,
            datatypes=FEATURES_DATATYPES,
            bonus_objectives=["Aerodynamic Drag"]
        )
        problem = MultiObjectiveProblem(data_package, predict, CONSTRAINT_FUNCTIONS)
        generator = LoggingGenerator(problem, OPTIMIZER_POPULATION)
        return generator

    def _get_bike_by_id(self, seed_bike_id):
        seed_bike = SEED_BIKES_MAP.get(str(seed_bike_id))
        validate(seed_bike is not None, f"Invalid seed bike ID [{seed_bike_id}]")
        return seed_bike

    def _get_body_dimensions_by_id(self, rider_id):
        rider = RIDERS_MAP.get(str(rider_id))
        if rider is None:
            raise UserInputException(f"Invalid rider ID [{rider_id}]")
        return rider
