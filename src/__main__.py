from azure.devops.v7_1.pipelines.pipelines_client import PipelinesClient
from parsers.get_last_attempt_to_deliver import get_last_attempt_to_deliver
from models import ArgumentParseResult
from arts.process_time_logo import process_time_logo

# azure_devops_organization = 'organization'
# personal_access_token = ''
# project = 'project'
# pipeline_id = 23
# 
# pipelines_client = PipelinesClient(f'https://dev.azure.com/{azure_devops_organization}', personal_access_token)
# runs = pipelines_client.list_runs(project, pipeline_id)
# previous_attempt = get_last_attempt_to_deliver(runs)

# print('hello world 2')
# 
# def parseArguments(argv) -> ArgumentParseResult:
#     

if __name__ == "__main__":
    print(process_time_logo)
    print('hello world 3')