from http import HTTPStatus

import werkzeug.exceptions
from flask import Flask, make_response

from exceptions import UserInputException

MESSAGE = "message"


def register_error_handlers(app: Flask):
    @app.errorhandler(UserInputException)
    def handle_user_error(exception: UserInputException):
        print(exception)
        return make_response({MESSAGE: exception.args[0]}, HTTPStatus.BAD_REQUEST)

    @app.errorhandler(werkzeug.exceptions.HTTPException)
    def handle_werkzeug(exception: werkzeug.exceptions.HTTPException):
        print(exception)
        return make_response({MESSAGE: exception.description}, exception.code)

    @app.errorhandler(Exception)
    def handle_internal_server_error(exception):
        print(exception)
        print(type(exception))
        return make_response({MESSAGE: "Something went wrong"}, HTTPStatus.INTERNAL_SERVER_ERROR)
