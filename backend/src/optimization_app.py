from flask import Flask, make_response, request
from flask.views import View
from flask_cors import CORS

from app_config.app_constants import APP_LOGGER
from app_config.app_parameters import LOGGING_LEVEL
from cad_services.cad_builder import BikeCadFileBuilder
from controller_advice import register_error_handlers
from exceptions import UserInputException
from fit_optimization.bike_optimizers import ErgonomicsOptimizer, AerodynamicsOptimizer, BikeOptimizer
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
ergonomics_optimizer = ErgonomicsOptimizer(image_analyzer)
aerodynamics_optimizer = AerodynamicsOptimizer(image_analyzer)
cad_builder = BikeCadFileBuilder()
app = build_app()


def register_optimization_endpoints(_app: Flask,
                                    optimization_type: str,
                                    _optimizer: BikeOptimizer):
    class OptimizeDimensions(View):
        def dispatch_request(self):
            _request = _get_json(request)
            return make_response(
                _optimizer.optimize_for_dimensions(
                    _request["seedBikeId"],
                    _request["riderDimensionsInches"],
                )
            )

    class OptimizeSeeds(View):
        def dispatch_request(self):
            _request = _get_json(request)
            return make_response(
                _optimizer.optimize_for_seeds(_request["seedBikeId"],
                                              _request["riderId"]))

    class OptimizeImage(View):
        def dispatch_request(self):
            _request = _get_json(request)
            return make_response(
                _optimizer.optimize_for_image(_request["seedBikeId"],
                                              map_base64_image_to_bytes(_request["imageBase64"]),
                                              _request["riderHeight"])
            )

    _app.add_url_rule(endpoint(f"/{optimization_type}/optimize-dimensions"),
                      view_func=OptimizeDimensions.as_view(f"{optimization_type}_dimensions"),
                      methods=[POST])
    _app.add_url_rule(endpoint(f"/{optimization_type}/optimize-seeds"),
                      view_func=OptimizeSeeds.as_view(f"{optimization_type}_seeds"),
                      methods=[POST])
    _app.add_url_rule(endpoint(f"/{optimization_type}/optimize-custom-rider"),
                      view_func=OptimizeImage.as_view(f"{optimization_type}_image"),
                      methods=[POST])


def register_download_endpoint(_app: Flask):
    @_app.route(endpoint("/download-cad"), methods=[POST])
    def download_cad_file():
        _request = _get_json(request)
        response = make_response(cad_builder.build_cad_from_object(_request["bike"],
                                                                   _request["seedBikeId"]))
        response.headers["Content-Type"] = "application/xml"
        return response


def register_health_endpoint(_app: Flask):
    @_app.route(endpoint("/health"))
    def health():
        return make_response({"status": "UP"})


def register_all_optimization_endpoints(_app):
    register_optimization_endpoints(_app, "ergonomics", ergonomics_optimizer)
    register_optimization_endpoints(_app, "aerodynamics", aerodynamics_optimizer)
    register_download_endpoint(_app)
    register_health_endpoint(_app)


register_all_optimization_endpoints(app)
