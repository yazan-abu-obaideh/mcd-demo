import os

from app_config.app_constants import APP_LOGGER


def get_config(variable_name, default_value):
    value = os.getenv(variable_name, default_value)
    _log_config_value(value, variable_name)
    return value


def _log_config_value(value, variable_name):
    # this runs before the logging level is set. The default logging level is WARN
    APP_LOGGER.warn(f"Variable {variable_name} set to {value}")
