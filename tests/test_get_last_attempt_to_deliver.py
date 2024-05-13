from azure.devops.v7_1.pipelines.models import Run
from src.parsers.get_last_attempt_to_deliver import get_last_attempt_to_deliver
from tests.generate_test_run import generate_test_run


def test_only_current_run_exist_should_return_current_run():
    current_run = generate_test_run(3, 'succeeded')
    pipelines = [current_run]
    result = get_last_attempt_to_deliver(pipelines)
    assert result.id == current_run.id


def test_previous_run_was_successful_return_current_run():
    current_run = generate_test_run(3, 'succeeded')
    previous_run = generate_test_run(2, 'succeeded')
    pipelines = [current_run, previous_run]
    result = get_last_attempt_to_deliver(pipelines)
    assert result.id == current_run.id


def test_previous_run_was_failed_but_no_more_runs_return_previous_run():
    current_run = generate_test_run(3, 'succeeded')
    previous_run = generate_test_run(2, 'failed')
    pipelines = [current_run, previous_run]
    result = get_last_attempt_to_deliver(pipelines)
    assert result.id == previous_run.id


def test_previous_run_was_failed_return_failed_before_successful():
    current_run = generate_test_run(3, 'succeeded')
    previous_run = generate_test_run(2, 'failed')
    previous_run2 = generate_test_run(1, 'succeeded')
    pipelines = [current_run, previous_run, previous_run2]
    result = get_last_attempt_to_deliver(pipelines)
    assert result.id == previous_run.id


def test_two_previous_runs_both_failed_return_last_failed_before_successful():
    current_run = generate_test_run(3, 'succeeded')
    previous_run = generate_test_run(2, 'failed')
    previous_run2 = generate_test_run(1, 'failed')
    previous_run3 = generate_test_run(0, 'succeeded')
    pipelines = [current_run, previous_run, previous_run2, previous_run3]
    result = get_last_attempt_to_deliver(pipelines)
    assert result.id == previous_run2.id
