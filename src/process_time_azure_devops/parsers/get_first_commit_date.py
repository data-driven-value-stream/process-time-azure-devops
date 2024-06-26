from azure.devops.v7_1.build import Build
from azure.devops.v7_1.git import GitClient
from azure.devops.v7_1.git.models import GitPullRequest, GitPullRequestQuery, GitPullRequestQueryInput
import datetime
import json

from process_time_azure_devops.parsers.find_pr import find_pr


def get_first_commit_date(project: str, credentials: any, url: str, commit: str, build: Build) \
        -> (datetime.datetime, None | GitPullRequest):
    """
    Get the first commit date from the pull request if PR is empty
    will just use commit date.
    :rtype (datetime.datetime, None | GitPullRequest)
    """
    git_client = GitClient(url, credentials)
    query_input_last_merge_commit = GitPullRequestQueryInput(
        items=[commit],
        type="lastMergeCommit"
    )

    query = GitPullRequestQuery([query_input_last_merge_commit])
    query_result = git_client.get_pull_request_query(query, build.repository.id, project)
    print('PR Query result info:')
    print(json.dumps(query_result.as_dict(), sort_keys=True, indent=4))

    pr = find_pr(project, query_result=query_result, git_client=git_client, commit=commit, build=build)
    if pr is None:
        print('No pull request found for the commit')
        commit_info = git_client.get_commit(commit, build.repository.id, project)
        print('Commit info:')
        print(json.dumps(commit_info.as_dict(), sort_keys=True, indent=4))
        first_commit_time = commit_info.author.date
        print(f'First commit time: {first_commit_time}')
        return commit_info.author.date, pr
    else:
        return get_first_commit_date_from_pr(pr), pr


def get_first_commit_date_from_pr(pr: GitPullRequest) -> datetime.datetime:
    first_commit = pr.commits[len(pr.commits) - 1]
    print("First commit of the pull request:")
    print(json.dumps(first_commit.as_dict(), sort_keys=True, indent=4))
    first_commit_time = first_commit.author.date
    print(f'First commit time: {first_commit_time}')
    return first_commit_time
