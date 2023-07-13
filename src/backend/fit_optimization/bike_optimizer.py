import attrs
from decode_mcd import DataPackage, MultiObjectiveProblem, CounterfactualsGenerator

from backend.fit_optimization.optimization_constants import *
from backend.models.ergo_bike import ErgoBike


class BikeOptimizer:
    def __init__(self):
        pass

    def optimize(self, seed_bike: ErgoBike, user_dimensions):
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
