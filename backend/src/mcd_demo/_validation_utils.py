from mcd_demo.exceptions import UserInputException


def validate(condition: bool, exception_message: str):
    if not condition:
        raise UserInputException(exception_message)
