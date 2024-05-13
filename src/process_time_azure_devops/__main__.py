from azure.devops.v7_1.pipelines.pipelines_client import PipelinesClient
from process_time_azure_devops.parsers.get_last_attempt_to_deliver import get_last_attempt_to_deliver
from process_time_azure_devops.models.ArgumentParseResult import ArgumentParseResult
from process_time_azure_devops.arts.process_time_logo import process_time_logo
from msrest.authentication import BasicAuthentication
import getopt
import sys
import json


def display_help():
    print('main.py --org <azure-devops-organization> --token <personal_access_token> --project <project> --pipeline-id <pipeline_id>')


def parse_arguments(argv) -> ArgumentParseResult:
    azure_devops_organization: str | None = None
    personal_access_token: str | None = None
    project: str | None = None
    pipeline_id: int | None = None
    opts, args = getopt.getopt(argv, "h", ["org=", "token=", "project=", "pipeline-id=", "help"])
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

    print('========== Arguments: ==========')
    print(f'Azure DevOps Organization: {azure_devops_organization}')
    print(f'Personal Access Token: {("*" * len(personal_access_token))[:7]}')
    print(f'Project: {project}')
    print(f'Pipeline ID: {pipeline_id}')
    print('================================')
    return ArgumentParseResult(azure_devops_organization, personal_access_token, project, pipeline_id)


def calculate_process_tine(args: ArgumentParseResult) -> None:
    print('Calculating process time...')
    url = f'https://dev.azure.com/{args.azure_devops_organization}'
    print(f'Connecting to Azure DevOps Organization: {url}')
    credentials = BasicAuthentication(args.personal_access_token)
    pipelines_client = PipelinesClient(f'https://dev.azure.com/{args.azure_devops_organization}', credentials)
    runs = pipelines_client.list_runs(args.project, args.pipeline_id)
    previous_attempt = get_last_attempt_to_deliver(runs)
    print(json.dumps(previous_attempt.as_dict(), sort_keys=True, indent=4))
    print('Process time calculated!')


if __name__ == "__main__":
    print(process_time_logo)
    arguments = parse_arguments(sys.argv[1:])
    calculate_process_tine(arguments)
