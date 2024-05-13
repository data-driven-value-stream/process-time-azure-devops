from azure.devops.v7_1.pipelines.pipelines_client import PipelinesClient
from parsers.get_last_attempt_to_deliver import get_last_attempt_to_deliver
from models.ArgumentParseResult import ArgumentParseResult
from arts.process_time_logo import process_time_logo
import getopt
import sys


# pipelines_client = PipelinesClient(f'https://dev.azure.com/{azure_devops_organization}', personal_access_token)
# runs = pipelines_client.list_runs(project, pipeline_id)
# previous_attempt = get_last_attempt_to_deliver(runs)

# print('hello world 2')
# 

def help():
    print('main.py --org <azure-devops-organization> --token <personal_access_token> --project <project> --pipeline-id <pipeline_id>')


def parse_arguments(argv) -> ArgumentParseResult:
    azure_devops_organization: str | None = None
    personal_access_token: str | None = None
    project: str | None = None
    pipeline_id: int | None = None
    opts, args = getopt.getopt(argv, "hi:o:", ["org=", "token=", "project=", "pipeline-id="])
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help()
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
    print(f'Personal Access Token: {"*" * len(personal_access_token)}')
    print(f'Project: {project}')
    print(f'Pipeline ID: {pipeline_id}')
    print('================================')
    return ArgumentParseResult(azure_devops_organization, personal_access_token, project, pipeline_id)


if __name__ == "__main__":
    print(process_time_logo)
    arguments = parse_arguments(sys.argv[1:])
