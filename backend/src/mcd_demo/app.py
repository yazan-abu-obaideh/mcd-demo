import logging

from flask import Flask, make_response, request
from flask.views import View
from flask_cors import CORS

from mcd_demo.app_config.app_constants import APP_LOGGER
from mcd_demo.app_config.app_parameters import LOGGING_LEVEL
from mcd_demo.app_config.rendering_parameters import RENDERER_POOL_SIZE
from mcd_demo.cad_services.bikeCad_renderer import RenderingService
from mcd_demo.cad_services.cad_builder import BikeCadFileBuilder
from mcd_demo.controller_advice import register_error_handlers
from mcd_demo.exceptions import UserInputException
from mcd_demo.fit_optimization.bike_optimizers import ErgonomicsOptimizer, AerodynamicsOptimizer, BikeOptimizer
from mcd_demo.models.model_scheme_validations import map_base64_image_to_bytes
from mcd_demo.pose_analysis.pose_image_processing import PoserAnalyzer

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


def register_typed_optimization_endpoints(_app: Flask,
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


def register_download_clips_endpoint(_app: Flask):
    @_app.route(optimization_endpoint("/download-clips-cad"), methods=[POST])
    def download_clips_cad_file():
        _request = _get_json(request)
        response = make_response(CAD_BUILDER.build_cad_from_clips_object(_request["bike"]))
        response.headers["Content-Type"] = "application/xml"
        return response


def register_render_from_object_endpoint(_app: Flask, rendering_service: RenderingService):
    @_app.route(rendering_endpoint("/render-bike-object"), methods=["POST"])
    def render_bike_object():
        response = make_response(rendering_service.render_object(request.json["bike"],
                                                                 request.json["seedImageId"]))
        response.headers["Content-Type"] = "image/svg+xml"
        return response


def register_text_prompt_optimization_endpoint(_app: Flask, _any_bike_optimizer: BikeOptimizer):
    @_app.route(optimization_endpoint("/text-prompt"), methods=[POST])
    def optimize_text_prompt():
        _request = _get_json(request)
        return make_response(
            _any_bike_optimizer.optimize_text_prompt(_request["textPrompt"])
        )


def register_all_optimization_endpoints(_app: Flask):
    image_analyzer = PoserAnalyzer()
    ergonomics_optimizer = ErgonomicsOptimizer(image_analyzer)
    aerodynamics_optimizer = AerodynamicsOptimizer(image_analyzer)
    register_typed_optimization_endpoints(_app, "ergonomics", ergonomics_optimizer)
    register_typed_optimization_endpoints(_app, "aerodynamics", aerodynamics_optimizer)
    register_text_prompt_optimization_endpoint(_app, ergonomics_optimizer)
    register_download_endpoint(_app)
    register_download_clips_endpoint(_app)


def register_render_clips_endpoint(_app: Flask, rendering_service: RenderingService):
    @_app.route(rendering_endpoint("/render-clips-bike"), methods=["POST"])
    def render_clips_bike():
        response = make_response(rendering_service.render_clips(request.json["bike"]))
        response.headers["Content-Type"] = "image/svg+xml"
        return response


def register_all_rendering_endpoints(_app: Flask):
    rendering_service = RenderingService(RENDERER_POOL_SIZE, cad_builder=CAD_BUILDER)
    register_render_from_object_endpoint(_app, rendering_service)
    register_render_clips_endpoint(_app, rendering_service)


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
