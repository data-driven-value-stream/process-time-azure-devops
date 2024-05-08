from azure.devops.v7_1.pipelines.models import Pipeline


def get_last_attempt_to_deliver(pipelines: [Pipeline]) -> Pipeline:
    """Get the last attempt to deliver from the list of pipelines."""
    return 0