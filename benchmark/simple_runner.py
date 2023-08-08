import base64
import concurrent.futures
import json
import os.path
import time

import requests


def get_resource_path(file_name):
    return os.path.join(os.path.dirname(__file__), "resources", file_name)


def post_optimization_request(base_url):
    resource_path = get_resource_path("dude.jpeg")
    with open(resource_path, "rb") as file:
        file_data = str(base64.b64encode(file.read()), "utf-8")
        url = f"{base_url}/api/v1/optimize-seed"
        headers = headers = {"Content-Type": "application/json"}
        data = {"cameraHeight": 75, "personHeight": 75,
                "seedBikeId": 3, "imageBase64": file_data}
        json_data = json.dumps(data)
        start = time.time()
        print("Started!")
        result = requests.post(url,
                               headers=headers,
                               data=json_data)
        print(result.text)
        print(result.content)
    return result.status_code, time.time() - start


def run_benchmark(base_url, concurrent_requests):
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_requests)
    future_results = []
    for _ in range(concurrent_requests):
        future_results.append(executor.submit(post_optimization_request, base_url))
    for result in future_results:
        print(result.result())


if __name__ == "__main__":
    bench_start = time.time()
    run_benchmark("http://161.35.112.82", concurrent_requests=10)
    print(f"Total runtime: {time.time() - bench_start}")
