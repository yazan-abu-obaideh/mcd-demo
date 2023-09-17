import logging

from flask import Flask, make_response, request
from flask.views import View
from flask_cors import CORS

from app_config.app_constants import APP_LOGGER
from app_config.app_parameters import LOGGING_LEVEL
from app_config.rendering_parameters import RENDERER_POOL_SIZE
from cad_services.bikeCad_renderer import RenderingService
from cad_services.cad_builder import BikeCadFileBuilder
from controller_advice import register_error_handlers
from exceptions import UserInputException
from fit_optimization.bike_optimizers import ErgonomicsOptimizer, AerodynamicsOptimizer, BikeOptimizer
from models.model_scheme_validations import map_base64_image_to_bytes
from pose_analysis.pose_image_processing import PoserAnalyzer

POST = "POST"
CAD_BUILDER = BikeCadFileBuilder()


def _get_json(_request):
    if not _request.is_json:
        raise UserInputException("Request payload should be of type application/json")
    return _request.json


def _configure_logger():
    APP_LOGGER.setLevel(LOGGING_LEVEL)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOGGING_LEVEL)
    APP_LOGGER.addHandler(console_handler)
    APP_LOGGER.info(f"Logging level set to {logging.getLevelName(LOGGING_LEVEL)}")


def build_app() -> Flask:
    _configure_logger()
    _app = Flask(__name__)
    CORS(_app)
    register_error_handlers(_app)
    return _app


def endpoint(suffix):
    return f"/api/v1{suffix}"


def optimization_endpoint(suffix):
    return endpoint(f"/optimization{suffix}")


def rendering_endpoint(suffix):
    return endpoint(f"/rendering{suffix}")


def register_health_endpoint(_app: Flask):
    @_app.route(endpoint("/health"))
    def health():
        return make_response({"status": "UP"})


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

    _app.add_url_rule(optimization_endpoint(f"/{optimization_type}/optimize-dimensions"),
                      view_func=OptimizeDimensions.as_view(f"{optimization_type}_dimensions"),
                      methods=[POST])
    _app.add_url_rule(optimization_endpoint(f"/{optimization_type}/optimize-seeds"),
                      view_func=OptimizeSeeds.as_view(f"{optimization_type}_seeds"),
                      methods=[POST])
    _app.add_url_rule(optimization_endpoint(f"/{optimization_type}/optimize-custom-rider"),
                      view_func=OptimizeImage.as_view(f"{optimization_type}_image"),
                      methods=[POST])


def register_download_endpoint(_app: Flask):
    @_app.route(optimization_endpoint("/download-cad"), methods=[POST])
    def download_cad_file():
        _request = _get_json(request)
        response = make_response(CAD_BUILDER.build_cad_from_object(_request["bike"],
                                                                   _request["seedBikeId"]))
        response.headers["Content-Type"] = "application/xml"
        return response


def register_render_from_object_endpoint(_app: Flask, rendering_service: RenderingService):
    @_app.route(rendering_endpoint("/render-bike-object"), methods=["POST"])
    def render_bike_object():
        response = make_response(rendering_service.render_object(request.json["bike"],
                                                                 request.json["seedImageId"]))
        response.headers["Content-Type"] = "image/svg+xml"
        return response


def register_all_optimization_endpoints(_app):
    image_analyzer = PoserAnalyzer()
    ergonomics_optimizer = ErgonomicsOptimizer(image_analyzer)
    aerodynamics_optimizer = AerodynamicsOptimizer(image_analyzer)
    register_optimization_endpoints(_app, "ergonomics", ergonomics_optimizer)
    register_optimization_endpoints(_app, "aerodynamics", aerodynamics_optimizer)
    register_download_endpoint(_app)


def register_all_rendering_endpoints(_app: Flask):
    rendering_service = RenderingService(RENDERER_POOL_SIZE, cad_builder=CAD_BUILDER)
    register_render_from_object_endpoint(_app, rendering_service)


def build_base_app() -> Flask:
    app = build_app()
    register_health_endpoint(app)
    return app


def build_full_app() -> Flask:
    app = build_base_app()
    register_all_rendering_endpoints(app)
    register_all_optimization_endpoints(app)
    return app


def build_optimization_app():
    app = build_base_app()
    register_all_optimization_endpoints(app)
    return app


def build_rendering_app():
    app = build_base_app()
    register_all_rendering_endpoints(app)
    return app
