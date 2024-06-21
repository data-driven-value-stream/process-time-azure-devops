from azure.devops.v7_1.git.models import GitPullRequest
import datetime
import json


def get_first_commit_date_from_pr(pr: GitPullRequest) -> datetime.datetime:
    first_commit = pr.commits[len(pr.commits) - 1]
    print("First commit of the pull request:")
    print(json.dumps(first_commit.as_dict(), sort_keys=True, indent=4))
    first_commit_time = first_commit.author.date
    print(f'First commit time: {first_commit_time}')
    return first_commit_time
