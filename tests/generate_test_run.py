from azure.devops.v7_1.pipelines.models import Run


def generate_test_run(id: int, result: str) -> Run:
    """ :param id: The id of the run can be succeeded | failed | canceled"""
    return Run(id, 'delivery pipeline', None, None, 'cd.yml', None, None, None, result, None, None, None, None )