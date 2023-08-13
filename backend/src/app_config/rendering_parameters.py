from app_config._config_utils import get_config

RENDERER_POOL_SIZE = int(get_config("RENDERER_POOL_SIZE", 1))
RENDERER_TIMEOUT = int(get_config("RENDERER_TIMEOUT", 25))
RENDERER_TIMEOUT_GRANULARITY = int(get_config("RENDERER_TIMEOUT_GRANULARITY", 1))
