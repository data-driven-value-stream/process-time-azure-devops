from azure.devops.v7_1.pipelines.models import Run
from src.parsers.get_last_attempt_to_deliver import get_last_attempt_to_deliver


def test_only_current_run_exist_should_return_current_run():
    current_run = Run(3, 'delivery pipeline', None, None, 'cd.yml', None, None, None, "succeeded", None, None, None, None )
    pipelines = [current_run]
    result = get_last_attempt_to_deliver(pipelines)
    assert result == current_run

def test_if_previous_run_was_successful_return_current_run():
    current_run = Run(3, 'delivery pipeline', None, None, 'cd.yml', None, None, None, "succeeded", None, None, None, None )
    previous_run = Run(2, 'delivery pipeline', None, None, 'cd.yml', None, None, None, "succeeded", None, None, None, None )
    pipelines = [current_run, previous_run]
    result = get_last_attempt_to_deliver(pipelines)
    assert result == current_run