from flask import Flask, make_response, request
from flask_cors import CORS

from app_config.app_constants import APP_LOGGER
from app_config.app_parameters import LOGGING_LEVEL
from cad_services.cad_builder import BikeCadFileBuilder
from controller_advice import register_error_handlers
from exceptions import UserInputException
from fit_optimization.bike_optimizer import BikeOptimizer
from models.model_scheme_validations import map_base64_image_to_bytes
from pose_analysis.pose_image_processing import PoserAnalyzer

POST = "POST"


def _get_json(_request):
    if not _request.is_json:
        raise UserInputException("Request payload should be of type application/json")
    return _request.json


def build_app() -> Flask:
    _app = Flask(__name__)
    CORS(_app)
    register_error_handlers(_app)
    APP_LOGGER.setLevel(LOGGING_LEVEL)
    return _app


def endpoint(url):
    return f"/api/v1/{url}"


image_analyzer = PoserAnalyzer()
optimizer = BikeOptimizer(image_analyzer)
cad_builder = BikeCadFileBuilder()
app = build_app()


@app.route(endpoint("/ergonomics/optimize-dimensions"), methods=[POST])
def optimize_ergo_specified_dimensions():
    _request = _get_json(request)
    return make_response(
        optimizer.optimize_ergonomics_for_dimensions(
            _request["seedBikeId"],
            _request["riderDimensionsInches"],
        )
    )


@app.route(endpoint("/aerodynamics/optimize-dimensions"), methods=[POST])
def optimize_aero_specified_dimensions():
    _request = _get_json(request)
    return make_response(
        optimizer.optimize_aerodynamics_for_dimensions(
            _request["seedBikeId"],
            _request["riderDimensionsInches"],
        )
    )


@app.route(endpoint("/download-cad"), methods=[POST])
def download_cad_file():
    _request = _get_json(request)
    response = make_response(cad_builder.build_cad_from_object(_request["bike"],
                                                               _request["seedBikeId"]))
    response.headers["Content-Type"] = "application/xml"
    return response


@app.route(endpoint("/ergonomics/optimize-custom-rider"), methods=[POST])
def optimize_custom_rider():
    _request = _get_json(request)
    return make_response(
        optimizer.optimize_ergonomics_for_custom_rider(_request["seedBikeId"],
                                                       map_base64_image_to_bytes(_request["imageBase64"]),
                                                       _request["personHeight"],
                                                       _request["cameraHeight"])
    )


@app.route(endpoint("/aerodynamics/optimize-custom-rider"), methods=[POST])
def optimize_aerodynamics_custom_rider():
    _request = _get_json(request)
    return make_response(
        optimizer.optimize_aerodynamics_for_custom_rider(_request["seedBikeId"],
                                                         map_base64_image_to_bytes(_request["imageBase64"]),
                                                         _request["personHeight"],
                                                         _request["cameraHeight"])
    )


@app.route(endpoint("/ergonomics/optimize-seeds"), methods=[POST])
def optimize_seeds():
    _request = _get_json(request)
    return make_response(
        optimizer.optimize_ergonomics_for_seeds(_request["seedBikeId"],
                                                _request["riderId"])
    )


@app.route(endpoint("/aerodynamics/optimize-seeds"), methods=[POST])
def optimize_aerodynamics_seeds():
    _request = _get_json(request)
    return make_response(
        optimizer.optimize_aerodynamics_for_seeds(_request["seedBikeId"],
                                                  _request["riderId"])
    )


@app.route(endpoint("/health"))
def health():
    return make_response({"status": "UP"})
