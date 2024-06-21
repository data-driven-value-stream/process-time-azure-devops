from process_time_azure_devops.models.JsonResult import JsonResult
import json


def test_should_create_correct_json():
    json_result = JsonResult(
        "https://dev.azure.com/worldpwn/_git/process-time",
        63500,
        150,
        "https://dev.azure.com/worldpwn/process-time/_build/results?buildId=150",
        9,
        "https://dev.azure.com/worldpwn/process-time/_git/process-time/pullrequest/9"
    )
    as_json = json_result.to_json()

    expected_json_str = """
    {
        "repositoryUrl": "https://dev.azure.com/worldpwn/_git/process-time",
        "processTimeInMinutes": 63500,
        "productionBuildId": 150,
        "productionBuildUrl": "https://dev.azure.com/worldpwn/process-time/_build/results?buildId=150",
        "firstChangePullRequestId": 9,
        "firstChangePullRequestUrl": "https://dev.azure.com/worldpwn/process-time/_git/process-time/pullrequest/9"
    }
    """

    expected_json = json.loads(expected_json_str)
    actual_json = json.loads(as_json)

    assert expected_json == actual_json, "The JSON objects are not equal"

