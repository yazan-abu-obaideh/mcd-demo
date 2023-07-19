from flask import Flask, make_response, request
from flask_cors import CORS

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


app = build_app()
image_analyzer = PoserAnalyzer()
optimizer = BikeOptimizer(image_analyzer)


@app.route("/optimize-seed", methods=["POST"])
def optimize_seed_bike():
    _request = request.json
    return make_response(
        optimizer.optimize_seed_bike(_request["seedBikeId"],
                                     map_base64_image_to_bytes(_request["imageBase64"]),
                                     _request["personHeight"],
                                     _request["cameraHeight"])
    )


@app.route("/optimize", methods=["POST"])
def optimize():
    seed_bike = map_request_to_model(request.json["seed-bike"], ErgoBike)
    body_dimensions = map_request_to_model(request.json["body-dimensions"], BodyDimensions)
    res = optimizer.optimize(seed_bike, body_dimensions).to_dict("records")
    return make_response(res)


@app.route("/health")
def health():
    return make_response({"status": "UP"})


if __name__ == '__main__':
    app.run(debug=True)
