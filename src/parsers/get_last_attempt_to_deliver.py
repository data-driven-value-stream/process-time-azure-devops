import json

from azure.devops.v7_1.pipelines.models import Run


def get_last_attempt_to_deliver(runs: [Run]) -> Run:
    """Get the last attempt to deliver from the list of pipelines."""
    print(json.dumps([run.as_dict() for run in runs], sort_keys=True, indent=4))
    if len(runs) == 1:
        return runs[0]
    failed_runs = amount_of_failed_previous_runs(runs)
    if failed_runs == 0:
        return runs[0]
    else:
        if len(runs) == failed_runs:
            return runs[0]
        return runs[failed_runs]


def amount_of_failed_previous_runs(runs: [Run]) -> int:
    """Get the amount of failed previous runs and skipping the first one"""
    count = 0
    for element in runs[1:]:
        if element.result == 'succeeded':
            return count
        else:
            count += 1
    return count
