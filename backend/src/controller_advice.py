from http import HTTPStatus

import werkzeug.exceptions
from flask import Flask, make_response

from exceptions import UserInputException, InternalError

MESSAGE = "message"


def register_error_handlers(app: Flask):
    @app.errorhandler(UserInputException)
    def handle_user_error(exception: UserInputException):
        print(exception)
        return _make_error_response(exception.args[0], HTTPStatus.BAD_REQUEST)

    @app.errorhandler(InternalError)
    def handle_internal_error(exception: InternalError):
        print(exception)
        return _make_error_response(exception.args[0], HTTPStatus.INTERNAL_SERVER_ERROR)

    @app.errorhandler(werkzeug.exceptions.HTTPException)
    def handle_werkzeug(exception: werkzeug.exceptions.HTTPException):
        print(exception)
        return _make_error_response(exception.description, exception.code)

    @app.errorhandler(Exception)
    def handle_internal_server_error(exception):
        print(exception)
        return _make_error_response("Something went wrong", HTTPStatus.INTERNAL_SERVER_ERROR)

    def _make_error_response(message, status_code):
        return make_response({MESSAGE: message}, status_code)
