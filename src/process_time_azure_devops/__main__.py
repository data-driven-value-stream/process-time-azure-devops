from process_time_azure_devops.models.ArgumentParseResult import ArgumentParseResult
from process_time_azure_devops.arts.process_time_logo import process_time_logo
from process_time_azure_devops.flows.get_flow import get_flow
import getopt
import sys


def display_help():
    print('Welcome to azure-devops-process-time help!')
    print('This script calculates the process time between the first commit of the pull request and the deployment.')
    print('For Trunk-Based Development use this arguments:')
    print('--org <azure-devops-organization> --token <personal_access_token> --project <project> '
          '--pipeline-id <pipeline_id> --current-run-id <current_run_id>')
    print('For GitFlow Development use this arguments:')
    print('--org <azure-devops-organization> --token <personal_access_token> --project <project> '
          '--pipeline-id <pipeline_id> --current-run-id <current_run_id> '
          '--production-branch-name <production_branch_name> --development-branch-name <development_branch_name>')


def parse_arguments(argv) -> ArgumentParseResult:
    azure_devops_organization: str | None = None
    personal_access_token: str | None = None
    project: str | None = None
    pipeline_id: int | None = None
    current_run_id: int | None = None
    production_branch_name: str | None = None
    development_branch_name: str | None = None

    opts, args = getopt.getopt(argv, "h", [
        "org=", "token=", "project=", "pipeline-id=", "current-run-id=",
        "production-branch-name=", "development-branch-name=",
        "help"])

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
        elif opt in "--production-branch-name":
            production_branch_name = arg
        elif opt in "--development-branch-name":
            development_branch_name = arg

    print('========== Arguments: ==========')
    print(f'Azure DevOps Organization: {azure_devops_organization}')
    print(f'Personal Access Token: {("*" * len(personal_access_token))[:7]}')
    print(f'Project: {project}')
    print(f'Pipeline ID: {pipeline_id}')
    print(f'Current Run ID: {current_run_id}')
    print(f'Production Branch Name: {production_branch_name}')
    print(f'Development Branch Name: {development_branch_name}')
    print('================================')
    return ArgumentParseResult(
        azure_devops_organization=azure_devops_organization,
        personal_access_token=personal_access_token,
        project=project,
        pipeline_id=pipeline_id,
        current_run_id=current_run_id,
        production_branch_name=production_branch_name,
        development_branch_name=development_branch_name)


if __name__ == "__main__":
    print(process_time_logo)
    arguments = parse_arguments(sys.argv[1:])
    flow = get_flow(arguments)
    process_time_result = flow.calculate_process_time()
    print('========== Result: ==========')
    print(process_time_result.to_json())
    print('=============================')
    with open(f'process_time_result_{arguments.current_run_id}.json', 'w') as f:
        f.write(process_time_result.to_json())
