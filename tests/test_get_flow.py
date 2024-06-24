from process_time_azure_devops.flows.get_flow import get_flow
from process_time_azure_devops.models.ArgumentParseResult import ArgumentParseResult
from process_time_azure_devops.flows.TrunkBasedFlow import TrunkBasedFlow
from process_time_azure_devops.flows.GitFlow import GitFlow
import pytest


def test_pass_production_branch_name_and_development_branch_name_should_return_git_flow():
    args = ArgumentParseResult(
        azure_devops_organization='azure',
        personal_access_token='token',
        project='project',
        pipeline_id=1,
        current_run_id=1,
        production_branch_name='production',
        development_branch_name='development')
    flow = get_flow(args)
    assert isinstance(flow, GitFlow)


def test_pass_none_return_trunk_based_flow():
    args = ArgumentParseResult(
        azure_devops_organization='azure',
        personal_access_token='token',
        project='project',
        pipeline_id=1,
        current_run_id=1,
        production_branch_name=None,
        development_branch_name=None)
    flow = get_flow(args)
    assert isinstance(flow, TrunkBasedFlow)


def test_pass_production_branch_name_and_development_branch_none_should_throw():
    args = ArgumentParseResult(
        azure_devops_organization='azure',
        personal_access_token='token',
        project='project',
        pipeline_id=1,
        current_run_id=1,
        production_branch_name='some_name',
        development_branch_name=None)
    with pytest.raises(ValueError) as exc_info:
        flow = get_flow(args)
        raise ValueError()

