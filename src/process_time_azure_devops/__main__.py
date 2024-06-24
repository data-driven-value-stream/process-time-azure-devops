from azure.devops.v7_1.pipelines.pipelines_client import PipelinesClient
from azure.devops.v7_1.build.build_client import BuildClient
from azure.devops.v7_1.git.git_client import GitClient
from azure.devops.v7_1.git.models import GitPullRequestQuery, GitPullRequestQueryInput
from process_time_azure_devops.parsers.get_last_attempt_to_deliver import get_last_attempt_to_deliver
from process_time_azure_devops.models.ArgumentParseResult import ArgumentParseResult
from process_time_azure_devops.models.JsonResult import JsonResult
from process_time_azure_devops.arts.process_time_logo import process_time_logo
from process_time_azure_devops.parsers.find_pr import find_pr
from process_time_azure_devops.parsers.get_first_commit_date_from_pr import get_first_commit_date_from_pr
from process_time_azure_devops.flows.get_flow import get_flow
from msrest.authentication import BasicAuthentication
import getopt
import sys
import json
import math


def display_help():
    print('main.py --org <azure-devops-organization> --token <personal_access_token> --project <project> '
          '--pipeline-id <pipeline_id> --current-run-id <current_run_id>')


def parse_arguments(argv) -> ArgumentParseResult:
    azure_devops_organization: str | None = None
    personal_access_token: str | None = None
    project: str | None = None
    pipeline_id: int | None = None
    current_run_id: int | None = None
    opts, args = getopt.getopt(argv, "h", ["org=", "token=", "project=", "pipeline-id=", "current-run-id=", "help"])
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            display_help()
            sys.exit()
        elif opt in "--org":
            azure_devops_organization = arg
        elif opt in "--token":
            personal_access_token = arg
        elif opt in "--project":
            project = arg
        elif opt in "--pipeline-id":
            pipeline_id = int(arg)
        elif opt in "--current-run-id":
            current_run_id = int(arg)

    print('========== Arguments: ==========')
    print(f'Azure DevOps Organization: {azure_devops_organization}')
    print(f'Personal Access Token: {("*" * len(personal_access_token))[:7]}')
    print(f'Project: {project}')
    print(f'Pipeline ID: {pipeline_id}')
    print(f'Current Run ID: {current_run_id}')
    print('================================')
    return ArgumentParseResult(azure_devops_organization, personal_access_token, project, pipeline_id, current_run_id)


if __name__ == "__main__":
    print(process_time_logo)
    arguments = parse_arguments(sys.argv[1:])
    flow = get_flow(arguments)
    process_time_result = flow.calculate_process_time()
    print('========== Result: ==========')
    print(process_time_result.to_json())
    print('=============================')
