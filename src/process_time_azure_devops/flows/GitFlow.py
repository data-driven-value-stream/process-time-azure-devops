import json

from azure.devops.v7_1.build import BuildClient
from azure.devops.v7_1.pipelines import PipelinesClient
from msrest.authentication import BasicAuthentication
from process_time_azure_devops.models.ArgumentParseResult import ArgumentParseResult
from process_time_azure_devops.models.JsonResult import JsonResult
from process_time_azure_devops.flows.Flow import Flow


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

        build = build_client.get_build(self.args.project, self.args.current_run_id)
        print('Current Build info:')
        print(json.dumps(build.as_dict(), sort_keys=True, indent=4))


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
        # Find the previous build from production branch
        # Get index of the current build
        current_build = next((build for build in prod_branches_builds if build.id == self.args.current_run_id),
                                   None)
        if current_build is None:
            raise ValueError(f'Current build not found in production branch {self.args.current_run_id}')

        print(json.dumps(current_build.as_dict(), sort_keys=True, indent=4))


        # Get pipeline runs
        # pipelines_client = PipelinesClient(url, credentials)
        # runs = pipelines_client.list_runs(self.args.project, self.args.pipeline_id)
        # for run in runs:
        #     print(json.dumps(run.as_dict(), sort_keys=True, indent=4))

        # Get builds that where source_branch == development_branch_name
        # builds = (build_client.get_builds(self.args.project,
        #                                  definitions=[self.args.pipeline_id],
        #                                  branch_name=f"refs/heads/{self.args.development_branch_name}"))
        # print(f'Builds info (source_branch {self.args.development_branch_name})')
        # for b in builds:
        #     print(json.dumps(b.as_dict(), sort_keys=True, indent=4))
        # return 1
