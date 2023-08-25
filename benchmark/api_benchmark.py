import concurrent.futures
import json
import os.path
import random
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
    rendering_workers: int
    optimization_workers: int
    max_concurrent_requests: int


@attrs.define(frozen=True)
class RunResults:
    optimization_run_results: List[TimedServerResponse]
    rendering_run_results: List[TimedServerResponse]
    interleaved_run_results: List[TimedServerResponse]
    interleaving_mode_description: str
    total_requests_processed: int
    total_runtime_seconds: float


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
    response = TimedServerResponse(result.status_code, finished)
    print(response)
    return response


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
    url = f"{base_url}/api/v1/ergonomics/optimize-seeds"
    data = {"riderId": "1", "seedBikeId": "3"}
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


def run_full_benchmark(base_rul,
                       max_concurrent_requests,
                       total_optimization_requests,
                       total_rendering_requests,
                       total_interleaved_requests,
                       node_description,
                       optimization_workers,
                       rendering_workers,
                       ):
    benchmark_start = time.time()
    (optimization_run_results, rendering_run_results,
     interleaved_run_results) = _run_all_benchmarks(base_rul, max_concurrent_requests, total_optimization_requests,
                                                    total_rendering_requests, total_interleaved_requests)
    total_runtime = time.time() - benchmark_start
    print(f"Total runtime: {total_runtime}")
    metadata = RunMetadata(node_description=node_description,
                           optimization_workers=optimization_workers,
                           rendering_workers=rendering_workers,
                           max_concurrent_requests=max_concurrent_requests,
                           timestamp_start_epoch=benchmark_start,
                           )
    run_results = RunResults(
        optimization_run_results=optimization_run_results,
        rendering_run_results=rendering_run_results,
        interleaved_run_results=interleaved_run_results,
        interleaving_mode_description="Random",
        total_runtime_seconds=total_runtime,
        total_requests_processed=(total_optimization_requests + total_rendering_requests + total_interleaved_requests)
    )
    with open(f"results/benchmark-results-{time.time()}-{str(uuid.uuid4())}.txt", "w") as result_file:
        # noinspection PyTypeChecker
        json.dump({
            "run_results": attrs.asdict(run_results),
            "run_metadata": attrs.asdict(metadata)
        }, result_file)


def _run_all_benchmarks(base_rul, max_concurrent_requests, total_optimization_requests, total_rendering_requests,
                        total_interleaved_requests):
    optimization_run_results = run_request_benchmark(base_rul,
                                                     post_optimization_request,
                                                     total_requests=total_optimization_requests,
                                                     max_concurrent_requests=max_concurrent_requests)
    rendering_run_results = run_request_benchmark(base_rul,
                                                  post_render_request,
                                                  total_requests=total_rendering_requests,
                                                  max_concurrent_requests=max_concurrent_requests)
    interleaved_run_results = run_request_benchmark(base_rul,
                                                    lambda url: random.choice(
                                                        [post_optimization_request, post_render_request])(url),
                                                    total_requests=total_interleaved_requests,
                                                    max_concurrent_requests=max_concurrent_requests
                                                    )
    return optimization_run_results, rendering_run_results, interleaved_run_results
