from mcd_demo.app_config._config_utils import get_config

OPTIMIZER_GENERATIONS = int(get_config("OPTIMIZER_GENERATIONS", 55))
OPTIMIZER_POPULATION = int(get_config("OPTIMIZER_POPULATION", 85))
