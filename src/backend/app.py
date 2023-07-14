from flask import Flask, make_response, request
from flask_cors import CORS

from backend.exceptions import UserInputException
from backend.fit_optimization.bike_optimizer import BikeOptimizer
from backend.models.body_dimensions import BodyDimensions
from backend.models.ergo_bike import ErgoBike
from backend.models.model_scheme_validations import map_request_to_model

app = Flask(__name__)
CORS(app)
optimizer = BikeOptimizer()


@app.errorhandler(UserInputException)
def handleUserError(exception: UserInputException):
    return make_response({"message": exception.args[0]}, 400)


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
