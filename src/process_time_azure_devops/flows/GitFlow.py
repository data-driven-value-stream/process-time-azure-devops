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
        Calculate the process time for the Git Flow
        """
        return 1
