import base64
import concurrent.futures
import json
import os.path
import time

import requests


def get_resource_path(file_name):
    return os.path.join(os.path.dirname(__file__), "resources", file_name)


def _benchmark_post_request(url: str, data: dict):
    headers = {"Content-Type": "application/json"}
    json_data = json.dumps(data)
    start = time.time()
    print(f"Started at {start}!")
    result = requests.post(url,
                           headers=headers,
                           data=json_data)
    return result.status_code, time.time() - start


def post_render_request(base_url: str):
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


def post_optimization_request(base_url: str):
    with open(get_resource_path("dude.jpeg"), "rb") as file:
        file_data = str(base64.b64encode(file.read()), "utf-8")
    url = f"{base_url}/api/v1/optimize-seed"
    data = {"cameraHeight": 75, "personHeight": 75,
            "seedBikeId": 3, "imageBase64": file_data}
    return _benchmark_post_request(url, data)


def run_optimization_benchmark(base_url: str, runnable_request: callable, concurrent_requests: int):
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_requests)
    future_results = []
    for _ in range(concurrent_requests):
        future_results.append(executor.submit(runnable_request, base_url))
    for result in future_results:
        print(result.result())


if __name__ == "__main__":
    bench_start = time.time()
    run_optimization_benchmark("http://161.35.112.82",
                               post_render_request,
                               concurrent_requests=10)
    print(f"Total runtime: {time.time() - bench_start}")
