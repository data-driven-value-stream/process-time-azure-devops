from azure.devops.v7_1.pipelines.models import Run
from src.parsers.get_last_attempt_to_deliver import get_last_attempt_to_deliver
from tests.generate_test_run import generate_test_run

def test_only_current_run_exist_should_return_current_run():
    current_run = generate_test_run(3, 'succeeded')
    pipelines = [current_run]
    result = get_last_attempt_to_deliver(pipelines)
    assert result == current_run

def test_if_previous_run_was_successful_return_current_run():
    current_run = generate_test_run(3, 'succeeded')
    previous_run = generate_test_run(2, 'succeeded')
    pipelines = [current_run, previous_run]
    result = get_last_attempt_to_deliver(pipelines)
    assert result == current_run
