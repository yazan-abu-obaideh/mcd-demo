import time

from decode_mcd import DataPackage, MultiObjectiveProblem, CounterfactualsGenerator

from _validation_utils import validate
from fit_analysis.demoanalysis_wrapped import calculate_angles, to_body_vector
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

    def optimize_seed_bike(self, seed_bike_id: str, image: bytes, person_height: float, camera_height: float):
        seed_bike = self._get_bike_by_id(seed_bike_id)
        body_dimensions = self.image_analysis_service.analyze_bytes(camera_height, image)
        print(f"{person_height=}")
        return self.optimize(seed_bike, body_dimensions)

    def optimize(self, seed_bike: dict, user_dimensions: dict):
        # noinspection PyTypeChecker

        def predict(_bikes: pd.DataFrame):
            start = time.time()
            response = calculate_angles(_bikes.values, to_body_vector(user_dimensions))
            print(f"Took {time.time() - start}")
            return response

        # noinspection PyTypeChecker
        data_package = DataPackage(
            features_dataset=DESIGNS,
            predictions_dataset=PERFORMANCES,
            query_x=pd.DataFrame.from_records([seed_bike]),
            design_targets=TARGETS,
            datatypes=FEATURES_DATATYPES
        )
        problem = MultiObjectiveProblem(data_package, predict, [])
        generator = LoggingGenerator(problem, 300)
        generator.generate(25)

        sampling_start = time.time()
        bikes = generator.sample_with_weights(num_samples=10, cfc_weight=1, diversity_weight=1, gower_weight=1,
                                              avg_gower_weight=1, include_dataset=False)
        print(f"sampling took {time.time() - sampling_start}")
        return {"bikes": bikes.to_dict("records"), "logs": generator.logs_list}

    def _get_bike_by_id(self, seed_bike_id):
        seed_bike = SEED_BIKES_MAP.get(seed_bike_id)
        validate(seed_bike is not None, "Invalid seed bike ID")
        return seed_bike
