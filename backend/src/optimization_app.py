from flask import Flask, make_response, request
from flask_cors import CORS

from app_config.app_parameters import LOGGING_LEVEL
from app_constants import APP_LOGGER
from controller_advice import register_error_handlers
from fit_optimization.bike_optimizer import BikeOptimizer
from models.model_scheme_validations import map_base64_image_to_bytes
from pose_analysis.pose_image_processing import PoserAnalyzer


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
app = build_app()


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
    res = optimizer.optimize(request.json["seed-bike"], request.json["body-dimensions"]).to_dict("records")
    return make_response(res)


@app.route(endpoint("/health"))
def health():
    return make_response({"status": "UP"})
