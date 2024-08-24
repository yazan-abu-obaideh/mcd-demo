import os

from mcd_demo.app_config.app_constants import APP_LOGGER

INTEGER_PARSER = lambda x: int(x)
STRING_PARSER = lambda x: x
BOOLEAN_PARSER = lambda x: str(True).lower() == str(x).lower()


def get_config(variable_name: str, default_value, parser):
    value = parser(os.getenv(variable_name, default_value))
    _log_config_value(value, variable_name)
    return value


def _log_config_value(value, variable_name):
    # this runs before the logging level is set. The default logging level is WARN
    APP_LOGGER.warn(f"Variable {variable_name} set to {value}")
