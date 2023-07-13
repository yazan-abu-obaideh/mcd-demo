from flask import Flask

from backend.fit_optimization.bike_optimizer import BikeOptimizer

app = Flask(__name__)
optimizer = BikeOptimizer()


@app.route("/health")
def health():
    return {"status": "UP"}


if __name__ == '__main__':
    app.run(debug=True)
