from azure.devops.v7_1.git.models import GitPullRequestQuery
from azure.devops.v7_1.git.git_client import GitClient
from azure.devops.v7_1.build.models import Build
import json
import datetime


def find_pr(project: str,
            query_result: GitPullRequestQuery,
            git_client: GitClient,
            commit: str, build: Build) -> None | datetime.datetime:
    """Find the pull request that contains the commit and return the first commit date of the PR.
        If the result is None it means that run is caused by a commit not in a pull request.
    """
    if len(query_result.results) == 0 or (len(query_result.results) == 1 and query_result.results[0] == {}):
        print('No pull request found for the commit')
        return None
    # If PR is found
    # Get first commit of the pull request info
    pr_id = query_result.results[0][commit][0].pull_request_id
    pr = git_client.get_pull_request(build.repository.id, pr_id, project, include_commits=True)
    print('Pull request info:')
    print(json.dumps(pr.as_dict(), sort_keys=True, indent=4))

    first_commit = pr.commits[len(pr.commits) - 1]
    print("First commit of the pull request:")
    print(json.dumps(first_commit.as_dict(), sort_keys=True, indent=4))
    first_commit_time = first_commit.author.date
    print(f'First commit time: {first_commit_time}')
    return first_commit_time
