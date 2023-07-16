import attrs
from decode_mcd import DataPackage, MultiObjectiveProblem, CounterfactualsGenerator

from _validation_utils import validate
from fit_optimization.optimization_constants import *
from models.body_dimensions import BodyDimensions
from models.ergo_bike import ErgoBike
from pose_analysis.pose_image_processing import PoserAnalyzer


class BikeOptimizer:
    def __init__(self, image_analysis_service: PoserAnalyzer):
        self.image_analysis_service = image_analysis_service

    def optimize_seed_bike(self, seed_bike_id: str, image: bytes, person_height: float, camera_height: float):
        seed_bike = self._get_bike_by_id(seed_bike_id)
        body_dimensions = self.image_analysis_service.analyze_bytes(camera_height, image)
        print(f"{person_height=}")
        print(f"{camera_height=}")
        return self.optimize(seed_bike, body_dimensions)

    def optimize(self, seed_bike: ErgoBike, user_dimensions: BodyDimensions):
        user_dimensions = attrs.asdict(user_dimensions)

        def predict(bikes: pd.DataFrame):
            return pd.DataFrame.from_records(ANALYZER.get_bikes_fit(bikes.to_dict('records'),
                                                                    user_dimensions))

        data_package = DataPackage(
            features_dataset=DESIGNS,
            predictions_dataset=PERFORMANCES,
            query_x=pd.DataFrame.from_records([attrs.asdict(seed_bike)]),
            design_targets=TARGETS,
            datatypes=FEATURES_DATATYPES
        )
        problem = MultiObjectiveProblem(data_package, predict, [])
        generator = CounterfactualsGenerator(problem, 750, initialize_from_dataset=False, verbose=True)
        generator.generate(5)
        return generator.sample_with_weights(num_samples=10, cfc_weight=1, diversity_weight=1,
                                             gower_weight=1, avg_gower_weight=1, )

    def _get_bike_by_id(self, seed_bike_id):
        seed_bike = SEED_BIKES_MAP.get(seed_bike_id)
        validate(seed_bike is not None, "Invalid seed bike ID")
        return ErgoBike(**seed_bike)
