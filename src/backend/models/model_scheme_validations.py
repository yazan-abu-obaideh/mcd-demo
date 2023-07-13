from typing import get_type_hints, Type

from backend._validation_utils import validate
from backend.exceptions import UserInputException


def map_request_to_model(request: dict, model: Type):
    actual_keys = request.keys()
    scheme = _get_scheme(model)
    validated_request = {}
    for expected_key, expected_type in scheme.items():
        _validate_key_exists(expected_key, actual_keys)
        validated_request[expected_key] = _attempt_cast(request, expected_key, expected_type)
    return model(**validated_request)


def _attempt_cast(request, key, _type):
    try:
        return _type(request[key])
    except Exception:
        raise UserInputException(f"Invalid type for {key} - expected {_type.__name__}")


def _validate_key_exists(expected_key, actual_keys):
    validate(expected_key in actual_keys, f"Required parameter {expected_key} missing")


def _get_scheme(model):
    all_type_hints = get_type_hints(model.__init__)
    del all_type_hints["return"]
    return all_type_hints
