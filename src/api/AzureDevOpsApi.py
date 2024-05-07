class AzureDevOpsApi:
    def __init__(self, systemAccessToken: str, orgranistaion: str, project: str):
        print('create azure devops api')
        self.systemAccessToken = systemAccessToken
        self.organisation = orgranistaion
        self.project = project
    
    def getPipelineRuns(self, pipelineDefinitionId: str):
        print('get pipeline runs')
        return []