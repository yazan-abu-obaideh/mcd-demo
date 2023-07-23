from flask import Flask, make_response, request
from flask_cors import CORS

from app_config.service_parameters import RENDERER_POOL_SIZE
from bike_rendering.bikeCad_renderer import RenderingService
from controller_advice import register_error_handlers
from fit_optimization.bike_optimizer import BikeOptimizer
from models.body_dimensions import BodyDimensions
from models.ergo_bike import ErgoBike
from models.model_scheme_validations import map_request_to_model, map_base64_image_to_bytes
from pose_analysis.pose_image_processing import PoserAnalyzer


def build_app() -> Flask:
    _app = Flask(__name__)
    CORS(_app)
    register_error_handlers(_app)
    return _app


def endpoint(url):
    return f"/api/v1/{url}"


app = build_app()
image_analyzer = PoserAnalyzer()
optimizer = BikeOptimizer(image_analyzer)
rendering_service = RenderingService(RENDERER_POOL_SIZE)


@app.route(endpoint("/render-bike"), methods=["POST"])
def render_bike():
    return rendering_service.render(request.data.decode("utf-8"))


@app.route(endpoint("/render-bike-object"), methods=["POST"])
def render_bike_object():
    with open("../test/resources/bike.bcad", "r") as file:
        response = make_response(rendering_service.render(file.read()))
        response.headers["Content-Type"] = "image/svg+xml"
        return response


@app.route(endpoint("/optimize-seed"), methods=["POST"])
def optimize_seed_bike():
    _request = request.json
    return make_response(
        optimizer.optimize_seed_bike(_request["seedBikeId"],
                                     map_base64_image_to_bytes(_request["imageBase64"]),
                                     _request["personHeight"],
                                     _request["cameraHeight"])
    )


@app.route(endpoint("/optimize"), methods=["POST"])
def optimize():
    seed_bike = map_request_to_model(request.json["seed-bike"], ErgoBike)
    body_dimensions = map_request_to_model(request.json["body-dimensions"], BodyDimensions)
    res = optimizer.optimize(seed_bike, body_dimensions).to_dict("records")
    return make_response(res)


@app.route(endpoint("/health"))
def health():
    return make_response({"status": "UP"})
