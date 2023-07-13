import queue
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stdout
from io import StringIO
from time import sleep

from flask import Flask, stream_template, render_template

from backend.fit_optimization.bike_optimizer import BikeOptimizer

POISON_PILL = None

app = Flask(__name__)
optimizer = BikeOptimizer()


class StreamingStringIO(StringIO):
    def __init__(self, lines_queue: queue.Queue):
        super().__init__()
        self.lines_queue = lines_queue

    def write(self, __s: str) -> int:
        self.lines_queue.put(__s)
        sleep(0.001)
        if __s is not None:
            return super().write(__s)


@app.route("/optimize")
def optimize():
    results = queue.Queue()
    stream_writer = StreamingStringIO(results)
    executor = ThreadPoolExecutor(max_workers=1)

    def produce_results():
        with redirect_stdout(stream_writer):
            print("optimizer starting!")
            counterfactuals_dataframe = optimizer.optimize(
                seed_bike={"seat_x": -9, "seat_y": 27, "handle_bar_x": 16.5, "handle_bar_y": 25.5, "crank_length": 7, },
                user_dimensions={'height': 75, 'sh_height': 61.09855828510818, 'hip_to_ankle': 31.167514055725047,
                                 'hip_to_knee': 15.196207871637029, 'shoulder_to_wrist': 13.538605228960089,
                                 'arm_len': 16.538605228960087, 'tor_len': 26.931044229383136,
                                 'low_leg': 18.971306184088018,
                                 'up_leg': 15.196207871637029})
            results.put(POISON_PILL)
            return counterfactuals_dataframe.to_dict("records")

    def yield_results():
        while True:
            last_line = results.get()
            if last_line is POISON_PILL:
                break
            yield last_line

    future_result = executor.submit(produce_results)

    def get_final_result():
        yield future_result.result()

    return stream_template("index.html", logs=yield_results(), cfs=get_final_result())


@app.route("/health")
def health():
    return {"status": "UP"}


@app.route("/temp")
def internal():
    return render_template("does_not_exist.html")


if __name__ == '__main__':
    app.run(debug=True)
