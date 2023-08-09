from api_benchmark import TimedServerResponse, RunResults, RunMetadata
import json
import pandas as pd

with open("results/benchmark-results-3f54185b-a268-4fc3-b45e-af5fb5737984.txt", "r") as file:
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
