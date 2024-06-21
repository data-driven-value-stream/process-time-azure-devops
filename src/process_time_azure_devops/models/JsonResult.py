import json


class JsonResult:
    def __init__(self,
                 repository_url: str,
                 process_time_in_minutes: int,
                 production_build_id: int,
                 production_build_url: str,
                 first_change_pull_request_id: int | None,
                 first_change_pull_request_url: str | None):
        self.repositoryUrl = repository_url
        self.processTimeInMinutes = process_time_in_minutes
        self.productionBuildId = production_build_id
        self.productionBuildUrl = production_build_url
        self.firstChangePullRequestId = first_change_pull_request_id
        self.firstChangePullRequestUrl = first_change_pull_request_url

    def to_json(self) -> str:
        return json.dumps(self.__dict__)
