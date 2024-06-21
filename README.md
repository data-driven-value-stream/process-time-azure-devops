[![Publish](https://github.com/worldpwn/process-time-azure-devops/actions/workflows/publish.yml/badge.svg)](https://github.com/worldpwn/process-time-azure-devops/actions/workflows/publish.yml)
<a href="https://pypi.org/project/process-time-azure-devops/"><img alt="PyPI" src="https://img.shields.io/pypi/v/process-time-azure-devops"></a>

PR Checks:

[![Build Status](https://worldpwn.visualstudio.com/process-time/_apis/build/status%2Fgithub%2Fgithub-ci?repoName=data-driven-value-stream%2Fprocess-time-azure-devops&branchName=refs%2Fpull%2F23%2Fmerge)](https://worldpwn.visualstudio.com/process-time/_build/latest?definitionId=5&repoName=data-driven-value-stream%2Fprocess-time-azure-devops&branchName=refs%2Fpull%2F23%2Fmerge)
[![PR](https://github.com/data-driven-value-stream/process-time-azure-devops/actions/workflows/pr.yml/badge.svg)](https://github.com/data-driven-value-stream/process-time-azure-devops/actions/workflows/pr.yml)


<img width="1597" alt="image" src="https://github.com/worldpwn/process-time-azure-devops/assets/6351780/d8adb7ce-e284-48e2-a56b-65ead73b17a6">

# Tutorial
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
