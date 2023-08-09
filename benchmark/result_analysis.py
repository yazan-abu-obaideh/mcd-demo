from api_benchmark import TimedServerResponse, RunResults, RunMetadata
import json

with open("results/benchmark-results-3f54185b-a268-4fc3-b45e-af5fb5737984.txt", "r") as file:
    report = json.load(file)

results = RunResults(**report["run_results"])
metadata = RunMetadata(**report["run_metadata"])
print(results)
