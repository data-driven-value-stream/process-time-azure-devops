from process_time_azure_devops.flows.Flow import Flow


class GitFlow(Flow):
    """
    Git Flow
    """
    def calculate_process_time(self):
        """
        Calculate the process time for the Git Flow
        """
        return 1