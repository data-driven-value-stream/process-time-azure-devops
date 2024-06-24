from process_time_azure_devops.flows.Flow import Flow


class TrunkBasedFlow(Flow):
    """
    Trunk Based Flow
    """
    def calculate_process_time(self):
        """
        Calculate the process time for the Trunk Based Flow
        """
        return 1