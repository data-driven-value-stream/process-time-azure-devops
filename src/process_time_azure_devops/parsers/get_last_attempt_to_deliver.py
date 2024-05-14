import json

from azure.devops.v7_1.pipelines.models import Run


def get_last_attempt_to_deliver(current_run_id: int, runs: [Run]) -> Run:
    """Get the last attempt to deliver from the list of pipelines."""

    sliced_runs = slice_until_current_run_id(current_run_id, runs)
    if len(sliced_runs) == 1:
        return sliced_runs[0]
    failed_runs = amount_of_failed_previous_runs(sliced_runs)
    if failed_runs == 0:
        return sliced_runs[0]
    else:
        if len(sliced_runs) == failed_runs:
            return sliced_runs[0]
        return sliced_runs[failed_runs]


def amount_of_failed_previous_runs(runs: [Run]) -> int:
    """Get the amount of failed previous runs and skipping the first one"""
    count = 0
    for element in runs[1:]:
        if element.result == 'succeeded':
            return count
        else:
            count += 1
    return count


def slice_until_current_run_id(current_run_id: id, runs: [Run]):
    try:
        if runs[0].id == current_run_id:
            return runs
        index = next(i for i, run in enumerate(runs) if run.id == current_run_id)
    except StopIteration:
        return []
    return runs[index:]