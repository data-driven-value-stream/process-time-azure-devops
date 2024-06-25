import json
import math

from azure.devops.v7_1.build import BuildClient
from azure.devops.v7_1.pipelines import PipelinesClient
from msrest.authentication import BasicAuthentication
from process_time_azure_devops.models.ArgumentParseResult import ArgumentParseResult
from process_time_azure_devops.models.JsonResult import JsonResult
from process_time_azure_devops.flows.Flow import Flow
from process_time_azure_devops.parsers.get_first_commit_date import get_first_commit_date


class GitFlow(Flow):
    """
    Git Flow
    """

    def __init__(self, args: ArgumentParseResult):
        self.args = args

    def calculate_process_time(self) -> JsonResult:
        """
         Calculate the process time for the Trunk Based Flow.
         Calculate the process time between the first commit of the pull request to development branch
         to the deployment from production branch.
         :rtype datetime.timedelta Example: 0:43:09.283935
         """
        print('[Git Flow] Calculating process time...')
        url = f'https://dev.azure.com/{self.args.azure_devops_organization}'
        print(f'Connecting to Azure DevOps Organization: {url}')
        credentials = BasicAuthentication('', self.args.personal_access_token)

        # Get builds
        build_client = BuildClient(url, credentials)

        # IDEA:
        # Get current BUILD from production branch
        # Get previous BUILD from production branch
        # Look for the RUNS from development branch between them by id
        # If none find look for previous previous build from production branch
        # Repeat until find the build from development branch.

        # Doing IDEA:
        prod_branches_builds = (build_client.get_builds(self.args.project,
                                                        definitions=[self.args.pipeline_id],
                                                        branch_name=f"refs/heads/{self.args.production_branch_name}"))
        current_build = next((build for build in prod_branches_builds if build.id == self.args.current_run_id),
                             None)
        if current_build is None:
            raise ValueError(f'Current build not found in production branch {self.args.current_run_id}')

        print('Current Build info:')
        print(json.dumps(current_build.as_dict(), sort_keys=True, indent=4))

        # Let's find the previous build
        index_current_build = prod_branches_builds.index(current_build)
        if index_current_build == len(prod_branches_builds) - 1:
            raise ValueError('There is no previous build in production branch')

        previous_build = prod_branches_builds[index_current_build + 1]
        print('Previous Build info:')
        print(json.dumps(previous_build.as_dict(), sort_keys=True, indent=4))

        # Now we need to find FIRST build for development branch
        # where id is bigger than previous_build.
        dev_branches_builds = (build_client.get_builds(self.args.project,
                                                       definitions=[self.args.pipeline_id],
                                                       branch_name=f"refs/heads/{self.args.development_branch_name}"))

        development_build_right_after_last_successful_production_build = next(
            (build for build in reversed(dev_branches_builds)
             if previous_build.id < build.id < current_build.id),
            None)
        print('First Development Build after last successful info:')
        print(json.dumps(development_build_right_after_last_successful_production_build.as_dict(),
                         sort_keys=True, indent=4))

        (first_commit_date, pr) = get_first_commit_date(
            project=self.args.project,
            credentials=credentials,
            url=url,
            build=development_build_right_after_last_successful_production_build,
            commit=development_build_right_after_last_successful_production_build.source_version)

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
            production_build_id=current_build.id,
            production_build_url=repository_url.replace("/_git/process-time",
                                                        "") + f"/_build/results?buildId={current_build.id}",
            first_change_pull_request_id=first_change_pull_request_id,
            first_change_pull_request_url=first_change_pull_request_url
        )
        return result
