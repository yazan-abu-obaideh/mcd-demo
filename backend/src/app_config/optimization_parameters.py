from app_config._config_utils import get_config

OPTIMIZER_GENERATIONS = int(get_config("OPTIMIZER_GENERATIONS", 25))
OPTIMIZER_POPULATION = int(get_config("OPTIMIZER_POPULATION", 300))
