class ArgumentParseResult:
    def __init__(self, azure_devops_organization: str, personal_access_token: str, project: str, pipeline_id: int, current_run_id: int):
        self.azure_devops_organization = azure_devops_organization
        self.personal_access_token = personal_access_token
        self.project = project
        self.pipeline_id = pipeline_id
        self.current_run_id = current_run_id
