class ArgumentParseResult:
    def __init__(self,
                 azure_devops_organization: str,
                 personal_access_token: str,
                 project: str,
                 pipeline_id: int,
                 current_run_id: int,
                 production_branch_name: str | None,
                 development_branch_name: str | None):
        """
         :param str | None production_branch_name: Is used to determine if it is a GitFlow,
          if it is a Trunk Based should be None
        """
        self.azure_devops_organization = azure_devops_organization
        self.personal_access_token = personal_access_token
        self.project = project
        self.pipeline_id = pipeline_id
        self.current_run_id = current_run_id
        self.production_branch_name = production_branch_name
        self.development_branch_name = development_branch_name

