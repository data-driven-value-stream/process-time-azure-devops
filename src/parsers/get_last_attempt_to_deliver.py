from azure.devops.v7_1.pipelines.models import Run

def get_last_attempt_to_deliver(runs: [Run]) -> Run:
    """Get the last attempt to deliver from the list of pipelines."""
    if len(runs) == 1:
        return runs[0]
    return runs[0]