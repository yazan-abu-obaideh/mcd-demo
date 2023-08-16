import json

import pandas as pd

from api_benchmark import RunResults, RunMetadata

with open("results/benchmark-results-1691755263.381678-33df6c4f-ec9a-4c3c-8ecd-553e911f6bb3.txt", "r") as file:
    report = json.load(file)

results = RunResults(**report["run_results"])
metadata = RunMetadata(**report["run_metadata"])


def print_description(run_results):
    if len(run_results) > 0:
        print(pd.DataFrame.from_records(run_results).describe())
    else:
        print("NOT RUN")


print("*** Run Metadata ***")
print(metadata)
print("*** Overview ***")
print(f"TPS: {results.total_requests_processed / results.total_runtime_seconds}")
print("*** Optimization Results ***")
print_description(results.optimization_run_results)
print("*** Rendering Results ***")
print_description(results.rendering_run_results)
print("*** Interleaved Results ***")
print_description(results.interleaved_run_results)
