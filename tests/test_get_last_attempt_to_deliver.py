from azure.devops.v7_1.pipelines.models import Pipeline
from src.parsers.get_last_attempt_to_deliver import get_last_attempt_to_deliver


def test_no_pipelines_should():
    pipelines = []
    result = get_last_attempt_to_deliver(pipelines)
    assert result == 4
