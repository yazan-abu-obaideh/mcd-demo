import os

from app_constants import APP_LOGGER


def get_config(variable_name, default_value):
    value = os.getenv(variable_name, default_value)
    APP_LOGGER.info(f"Variable {variable_name} set to {value}")
    return value
