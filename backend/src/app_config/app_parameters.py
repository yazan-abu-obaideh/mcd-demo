import logging

from app_config._config_utils import get_config

LOGGING_LEVEL = get_config("APP_LOGGING_LEVEL", logging.INFO)
