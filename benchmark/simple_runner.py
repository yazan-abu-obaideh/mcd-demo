import base64
import concurrent.futures
import json
import os.path
import time
import uuid
from typing import List, Callable

import attrs
import requests


@attrs.define(frozen=True)
class TimedServerResponse:
    http_status_code: int
    time_elapsed_seconds: float


@attrs.define(frozen=True)
class RunMetadata:
    node_description: str
    timestamp_start_epoch: float
    total_runtime_seconds: float
    rendering_workers: int
    optimization_workers: int
    _max_concurrent_requests: int


@attrs.define(frozen=True)
class RunResults:
    optimization_run_results: List[TimedServerResponse]
    rendering_run_results: List[TimedServerResponse]
    interleaved_run_results: List[TimedServerResponse]
    interleaving_mode_description: str


def get_resource_path(file_name):
    return os.path.join(os.path.dirname(__file__), "resources", file_name)


def _benchmark_post_request(url: str, data: dict) -> TimedServerResponse:
    headers = {"Content-Type": "application/json"}
    json_data = json.dumps(data)
    start = time.time()
    print(f"Started at {start}!")
    result = requests.post(url,
                           headers=headers,
                           data=json_data)
    finished = time.time() - start
    print(f"Finished in {finished} seconds")
    return TimedServerResponse(result.status_code, finished)


def post_render_request(base_url: str) -> TimedServerResponse:
    url = f"{base_url}/api/v1/rendering/render-bike-object"
    data = {
        "bike": {
            "Crank length": 176.58964008607123,
            "DT Length": 636.1790000000001,
            "Handlebar style": 1,
            "Headset spacers": 15,
            "HT Angle": 72.1,
            "HT Length": 151.5568932026963,
            "HT LX": 54.3,
            "Saddle height": 380.64295349035007,
            "Seatpost LENGTH": 245.03384475430303,
            "ST Angle": 72.5,
            "ST Length": 300,
            "Stack": 565.6,
            "Stem angle": -0.006089748189444744,
            "Stem length": 102.067556188142
        },
        "seedImageId": "3"
    }
    return _benchmark_post_request(url, data)


def post_optimization_request(base_url: str) -> TimedServerResponse:
    with open(get_resource_path("dude.jpeg"), "rb") as file:
        file_data = str(base64.b64encode(file.read()), "utf-8")
    url = f"{base_url}/api/v1/optimize-seed"
    data = {"cameraHeight": 75, "personHeight": 75,
            "seedBikeId": 3, "imageBase64": file_data}
    return _benchmark_post_request(url, data)


def run_request_benchmark(base_url: str,
                          runnable_request: Callable[[str], TimedServerResponse],
                          total_requests: int,
                          max_concurrent_requests: int) -> List[TimedServerResponse]:
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent_requests)
    future_timed_responses = []
    timed_responses = []
    for _ in range(total_requests):
        future_timed_responses.append(executor.submit(lambda: runnable_request(base_url)))
    for future_timed_response in future_timed_responses:
        timed_response = future_timed_response.result()
        timed_responses.append(timed_response)
    return timed_responses


if __name__ == "__main__":
    _max_concurrent_requests = 5
    _total_requests = 10
    benchmark_start = time.time()
    optimization_run_results = run_request_benchmark("http://161.35.112.82",
                                                     post_optimization_request,
                                                     total_requests=_total_requests,
                                                     max_concurrent_requests=_max_concurrent_requests)
    total_runtime = time.time() - benchmark_start
    print(f"Total runtime: {total_runtime}")
    metadata = RunMetadata(node_description="Digital Ocean CPU-optimized node "
                                            "regular intel 8vCPUs 16GB $168/month",
                           optimization_workers=3,
                           rendering_workers=3,
                           max_concurrent_requests=_max_concurrent_requests,
                           timestamp_start_epoch=benchmark_start,
                           total_runtime_seconds=total_runtime
                           )
    run_results = RunResults(
        optimization_run_results=optimization_run_results,
        rendering_run_results=[],
        interleaved_run_results=[],
        interleaving_mode_description="NA"
    )
    with open(f"benchmark-results-{str(uuid.uuid4())}.txt", "w") as result_file:
        # noinspection PyTypeChecker
        json.dump({
            "run_results": attrs.asdict(run_results),
            "run_metadata": attrs.asdict(metadata)
        }, result_file)
