from mcd_demo.app_config._config_utils import get_config

OPTIMIZER_GENERATIONS = int(get_config("OPTIMIZER_GENERATIONS", 55))
OPTIMIZER_POPULATION = int(get_config("OPTIMIZER_POPULATION", 85))
SAMPLE_CLIPS_SUBSET = bool(get_config("SAMPLE_CLIPS_SUBSET", True))
