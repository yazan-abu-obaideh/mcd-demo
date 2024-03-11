from http import HTTPStatus

import werkzeug.exceptions
from flask import Flask, make_response

from mcd_demo.app_config.app_constants import APP_LOGGER
from mcd_demo.exceptions import UserInputException, InternalError

MESSAGE = "message"


def register_error_handlers(app: Flask):
    @app.errorhandler(UserInputException)
    def handle_user_error(exception: UserInputException):
        return _make_error_response(exception, exception.args[0], HTTPStatus.BAD_REQUEST)

    @app.errorhandler(InternalError)
    def handle_internal_error(exception: InternalError):
        return _make_error_response(exception, exception.args[0], HTTPStatus.INTERNAL_SERVER_ERROR)

    @app.errorhandler(werkzeug.exceptions.HTTPException)
    def handle_werkzeug(exception: werkzeug.exceptions.HTTPException):
        return _make_error_response(exception, exception.description, exception.code)

    @app.errorhandler(Exception)
    def handle_internal_server_error(exception):
        return _make_error_response(exception, "Something went wrong", HTTPStatus.INTERNAL_SERVER_ERROR)

    def _make_error_response(exception, returned_message, status_code):
        APP_LOGGER.error(exception)
        return make_response({MESSAGE: returned_message}, status_code)
