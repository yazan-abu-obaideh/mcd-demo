import logging

from mcd_demo.app_config._config_utils import get_config, STRING_PARSER

LOGGING_LEVEL = get_config("APP_LOGGING_LEVEL", logging.INFO, STRING_PARSER)
