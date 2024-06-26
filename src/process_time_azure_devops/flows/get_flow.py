from process_time_azure_devops.models.ArgumentParseResult import ArgumentParseResult
from process_time_azure_devops.flows.Flow import Flow
from process_time_azure_devops.flows.TrunkBasedFlow import TrunkBasedFlow
from process_time_azure_devops.flows.GitFlow import GitFlow


def get_flow(args: ArgumentParseResult) -> Flow:
    """
    Get the flow based on the arguments
    """
    if args.production_branch_name is None and args.development_branch_name is None:
        return TrunkBasedFlow(args)
    elif args.production_branch_name and args.development_branch_name:
        return GitFlow(args)
    else:
        raise ValueError('Cannot determine the flow based on the arguments provided. '
                         'For GitFlow, both production and deployment branch names should be provided. '
                         'For TrunkBasedFlow, both production and deployment branch names should be None.')
