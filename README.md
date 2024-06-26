
[![Publish](https://github.com/worldpwn/process-time-azure-devops/actions/workflows/publish.yml/badge.svg)](https://github.com/worldpwn/process-time-azure-devops/actions/workflows/publish.yml)
<a href="https://pypi.org/project/process-time-azure-devops/"><img alt="PyPI" src="https://img.shields.io/pypi/v/process-time-azure-devops"></a>

PR Checks:

[![Build Status](https://worldpwn.visualstudio.com/process-time/_apis/build/status%2Fgithub%2Fgithub-ci?repoName=data-driven-value-stream%2Fprocess-time-azure-devops&branchName=refs%2Fpull%2F23%2Fmerge)](https://worldpwn.visualstudio.com/process-time/_build/latest?definitionId=5&repoName=data-driven-value-stream%2Fprocess-time-azure-devops&branchName=refs%2Fpull%2F23%2Fmerge)
[![PR](https://github.com/data-driven-value-stream/process-time-azure-devops/actions/workflows/pr.yml/badge.svg)](https://github.com/data-driven-value-stream/process-time-azure-devops/actions/workflows/pr.yml)

**Process Time** - the time from a line change in the code to the deployment of the artefact created by this change to the production environment.

Full Documentation: [https://github.com/data-driven-value-stream/.github/wiki/Process-Time](https://github.com/data-driven-value-stream/.github/wiki/Process-Time)

# Tutorial

Here is an example [https://worldpwn.visualstudio.com/process-time/_build?definitionId=4](https://worldpwn.visualstudio.com/process-time/_build?definitionId=4)

## Azure Devops repository Access
To access repository in Azure DevOps with pipline access token you need either run pipeline.yml file from the repository itself or reference needed repository in reosource.

```yml
resources:
  repositories:
    - repository: process-time
      type: git
      name: process-time
      ref: main

steps:
- checkout: process-time
- checkout: self
- script: |
    # do something
  displayName: 'Can access both repositories'
  env:
    System.AccessToken: $(System.AccessToken)
```


## Example Trunk Based Development

```yml
resources:
  repositories:
    - repository: process-time
      type: git
      name: process-time
      ref: main

steps:
- checkout: process-time
- checkout: self
- script: |
    # Set Variables
    orgname="Azure DevOps Organization Name"
    echo "orgname=$orgname"
    token=$(System.AccessToken)
    project="Azure DevOps Project Name"
    echo "project=$project"
    pipeline_id=1
    echo "pipeline_id=$pipeline_id"
    current_run_id=23
    echo "current_run_id=$pipeline_id"
    
    # Install Dependencies    
    python -m pip install --upgrade pip
    pip install process-time-azure-devops==0.1.0
    pip install azure-devops=7.1.0b4
    
    # Run Process Time Package
    python src/process_time_azure_devops/__main__.py --org "$orgname" --token "$token" --project "$project" --pipeline-id "$pipeline_id" --current-run-id $current_run_id 
  displayName: 'Can access both repositories'
  env:
    System.AccessToken: $(System.AccessToken)

# To publish result use run id in file name
- publish: $(System.DefaultWorkingDirectory)/process-time-azure-devops/process_time_result_23.json
  artifact: process_time_result_23
```

## Example Git-Flow

```yml
resources:
  repositories:
    - repository: process-time
      type: git
      name: process-time
      ref: main

steps:
- checkout: process-time
- checkout: self
- script: |
    # Set Variables
    orgname="Azure DevOps Organization Name"
    echo "orgname=$orgname"
    token=$(System.AccessToken)
    project="Azure DevOps Project Name"
    echo "project=$project"
    pipeline_id=1
    echo "pipeline_id=$pipeline_id"
    current_run_id=23
    echo "current_run_id=$pipeline_id"
    
    # Install Dependencies    
    python -m pip install --upgrade pip
    pip install process-time-azure-devops==0.1.0
    pip install azure-devops=7.1.0b4
    
    # Run Process Time Package
    # Add argument for development and production branch names without 'refs/heads/'
    python src/process_time_azure_devops/__main__.py --org "$orgname" --token "$token" --project "$project" --pipeline-id "$pipeline_id" --current-run-id $current_run_id --production-branch-name "production" --development-branch-name "development" 
  displayName: 'Can access both repositories'
  env:
    System.AccessToken: $(System.AccessToken)

# To publish result use run id in file name
- publish: $(System.DefaultWorkingDirectory)/process-time-azure-devops/process_time_result_23.json
  artifact: process_time_result_23
```