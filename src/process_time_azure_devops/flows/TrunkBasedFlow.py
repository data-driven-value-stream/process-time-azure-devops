from process_time_azure_devops.flows.Flow import Flow
from azure.devops.v7_1.pipelines.pipelines_client import PipelinesClient
from azure.devops.v7_1.build.build_client import BuildClient
from azure.devops.v7_1.git.git_client import GitClient
from azure.devops.v7_1.git.models import GitPullRequestQuery, GitPullRequestQueryInput
from process_time_azure_devops.parsers.get_last_attempt_to_deliver import get_last_attempt_to_deliver
from process_time_azure_devops.models.ArgumentParseResult import ArgumentParseResult
from process_time_azure_devops.models.JsonResult import JsonResult
from process_time_azure_devops.parsers.find_pr import find_pr
from process_time_azure_devops.parsers.get_first_commit_date import get_first_commit_date
from msrest.authentication import BasicAuthentication
import json
import math


class TrunkBasedFlow(Flow):
    """
    Trunk Based Flow
    """

    def __init__(self, args: ArgumentParseResult):
        self.args = args

    def calculate_process_time(self) -> JsonResult:
        """
        Calculate the process time for the Trunk Based Flow.
        Calculate the process time between the first commit of the pull request and the deployment.
        :rtype datetime.timedelta Example: 0:43:09.283935
        """

        print('[Trunk-Based] Calculating process time...')
        url = f'https://dev.azure.com/{self.args.azure_devops_organization}'
        print(f'Connecting to Azure DevOps Organization: {url}')
        credentials = BasicAuthentication('', self.args.personal_access_token)

        # Get pipeline runs
        pipelines_client = PipelinesClient(url, credentials)
        runs = pipelines_client.list_runs(self.args.project, self.args.pipeline_id)
        previous_attempt = get_last_attempt_to_deliver(self.args.current_run_id, runs)
        print('Previous attempt to deliver:')
        print(json.dumps(previous_attempt.as_dict(), sort_keys=True, indent=4))

        # Get build info based on run
        build_client = BuildClient(url, credentials)
        build = build_client.get_build(self.args.project, previous_attempt.id)
        print('Build info:')
        print(json.dumps(build.as_dict(), sort_keys=True, indent=4))

        commit = build.source_version
        print(f'Commit: {commit}')

        # Get pull request that cause pipeline to run
        (first_commit_date, pr) = get_first_commit_date(
            project=self.args.project,
            credentials=credentials,
            url=url,
            commit=commit,
            build=build)

        # Get time difference between first commit and deployment
        current_run = build_client.get_build(self.args.project, self.args.current_run_id)
        print('Current run info:')
        print(json.dumps(current_run.as_dict(), sort_keys=True, indent=4))
        print(f'Current run time: {current_run.finish_time}')

        process_time = current_run.finish_time - first_commit_date
        print(f'Process time: {process_time}')
        print('Process time calculated!')

        repository_url = current_run.repository.url
        first_change_pull_request_id = None
        first_change_pull_request_url = None
        if pr is not None:
            first_change_pull_request_id = pr.pull_request_id
            first_change_pull_request_url = f"{repository_url}/pullrequest/{pr.pull_request_id}"

        result = JsonResult(
            repository_url=repository_url,
            process_time_in_minutes=math.ceil(process_time.total_seconds() / 60),
            production_build_id=build.id,
            production_build_url=repository_url.replace("/_git/process-time",
                                                        "") + f"/_build/results?buildId={build.id}",
            first_change_pull_request_id=first_change_pull_request_id,
            first_change_pull_request_url=first_change_pull_request_url
        )

        return result
