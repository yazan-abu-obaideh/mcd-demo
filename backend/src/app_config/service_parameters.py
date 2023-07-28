import os


def _get_config(variable_name, default_value):
    value = os.getenv(variable_name, default_value)
    print(f"Variable {variable_name} set to {value}")
    return value


RENDERER_POOL_SIZE = int(_get_config("RENDERER_POOL_SIZE", 3))
RENDERER_TIMEOUT = int(_get_config("RENDERER_TIMEOUT", 25))
RENDERER_TIMEOUT_GRANULARITY = int(_get_config("RENDERER_TIMEOUT_GRANULARITY", 1))
