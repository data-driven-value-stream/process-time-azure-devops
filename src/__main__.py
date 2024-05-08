from api.AzureDevOpsApi import AzureDevOpsApi

api = AzureDevOpsApi("test")

pipelineRuns = api.getPipelineRuns("test", "test", "test")



print('hello world 2')


