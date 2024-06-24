from process_time_azure_devops.flows.Flow import Flow
from azure.devops.v7_1.pipelines.pipelines_client import PipelinesClient
from azure.devops.v7_1.build.build_client import BuildClient
from azure.devops.v7_1.git.git_client import GitClient
from azure.devops.v7_1.git.models import GitPullRequestQuery, GitPullRequestQueryInput
from process_time_azure_devops.parsers.get_last_attempt_to_deliver import get_last_attempt_to_deliver
from process_time_azure_devops.models.ArgumentParseResult import ArgumentParseResult
from process_time_azure_devops.models.JsonResult import JsonResult
from process_time_azure_devops.parsers.find_pr import find_pr
from process_time_azure_devops.parsers.get_first_commit_date_from_pr import get_first_commit_date_from_pr
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
        git_client = GitClient(url, credentials)
        query_input_last_merge_commit = GitPullRequestQueryInput(
            items=[commit],
            type="lastMergeCommit"
        )

        query = GitPullRequestQuery([query_input_last_merge_commit])
        query_result = git_client.get_pull_request_query(query, build.repository.id, self.args.project)
        print('PR Query result info:')
        print(json.dumps(query_result.as_dict(), sort_keys=True, indent=4))

        # If query result is empty it means that run is caused by a commit not in a pull request
        # find first pr
        pr = find_pr(project=args.project, query_result=query_result, git_client=git_client, commit=commit, build=build)
        if pr is None:
            print('No pull request found for the commit')
            commit_info = git_client.get_commit(commit, build.repository.id, self.args.project)
            print('Commit info:')
            print(json.dumps(commit_info.as_dict(), sort_keys=True, indent=4))
            first_commit_time = commit_info.author.date
            print(f'First commit time: {first_commit_time}')
            first_commit_date = commit_info.author.date
        else:
            first_commit_date = get_first_commit_date_from_pr(pr)

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
            production_build_url=repository_url.replace("/_git/process-time", "") + f"/_build/results?buildId={build.id}",
            first_change_pull_request_id=first_change_pull_request_id,
            first_change_pull_request_url=first_change_pull_request_url
        )

        return result
