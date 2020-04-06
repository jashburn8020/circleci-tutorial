# CircleCI Tutorial

## Prerequisites

- [GitHub](https://github.com/) account
  - create a public repository for this tutorial, e.g., `circleci-tutorial`
  - clone the repository, and use it as your project directory
- [CircleCI](https://circleci.com/) account
  - sign up to CircleCI using your GitHub account
- [Codecov](https://codecov.io/) account

## Create small Python application

- Create and checkout a feature branch in your Git repository
- Create a virtual environment
  - `python3 -m venv venv`
  - `source venv/bin/activate`
- Install additional modules
  - coverage
- Write tests
  - [`test/test_maths.py`](test/test_maths.py)
- Run tests
  - `python -m unittest -v`
  - all the tests should fail
- Write implementation until the tests pass
  - [`src/maths.py`](src/maths.py)
- Run `coverage`
  - `coverage run -m unittest`
  - `coverage report`
- Generate requirements file
  - `pip freeze > requirements.txt`
  - see [`requirements.txt`](requirements.txt)
  - note: on Ubuntu, `pip freeze` includes the `pkg-resources==0.0.0` line, which needs to be removed
- Commit changes and push to GitHub

## Set up CircleCI

- Log in to CircleCI
- Click on the 'Projects' icon on the task bar
- Click 'Set Up Project' for the `circleci-tutorial` repository
- Select the 'Python' config template
- Click 'Start Building'
- When you are prompted 'Add this config to your repo', click 'Add Config'
  - this adds a `.circleci/config.yml` file to a new `circleci-project-setup` branch to your repo
  - the build will initially fail
- To see why it failed
  - click on 'FAILED' status > 'build-and-test'
- Note: by default, CircleCI will monitor and build all branches in the project
- Get the `config.yml` file into your feature branch
  - merge the `circleci-project-setup` branch to the `master` branch
  - rebase your feature branch against the `master` branch
    - (on your feature branch) `git rebase master`
- The default Python `config.yml` template:
  - `orbs`
    - available on CircleCI Cloud with `version: 2.1` config
    - shareable packages of configuration elements - jobs, commands and executors, etc.
    - immutable - once an orb has been published to a semantic version, the orb cannot be changed
    - see <https://circleci.com/orbs/registry/orb/circleci/python> for the `circleci/python@0.2.1` orb that is preset on the template
    - a registry of orbs is available at <https://circleci.com/orbs/registry/>
    - `python: circleci/python@0.2.1`
      - `python`: orb reference
      - `circleci/python@0.2.1`: fully-qualified orb reference
  - `jobs`
    - a collection of steps
    - comprised of one or more named jobs, e.g., `build-and-test`
    - `executor`
      - environment in which steps of a job will be run
      - possible executors include `docker` (Docker image), `machine` (a dedicated, ephemeral VM) and `macos` (a macOS environment on a VM)
      - `python/default`: the default executor defined in the `python` orb
        - uses `circleci/python:latest` Docker image, which _should be avoided_
          - see <https://circleci.com/docs/2.0/executor-types/#docker-image-best-practices>
      - pre-built CircleCI Docker images: <https://circleci.com/docs/2.0/circleci-images/>
      - CircleCI Dockerfiles: <https://github.com/CircleCI-Public/circleci-dockerfiles>
      - CircleCI Docker images: <https://hub.docker.com/u/circleci>
    - `steps`
      - a collection of executable commands that are run during a job
      - `checkout`
        - a special step used to check out source code
        - note: if you require doing git over HTTPS you should not use this step as it configures git to checkout over ssh
      - `python/xxx`
        - steps defined in the orb
        - see <https://circleci.com/orbs/registry/orb/circleci/python>
        - `python/load-cache`: load cached pip packages
        - `python/install-deps`: install packages from `requirements.txt` via pip
          - a virtual environment is not necessary in this step because the `python` orb already makes use of a Docker image
          - see:
            - <https://coderbook.com/@marcus/should-i-use-virtualenv-or-docker-containers-with-python/>
            - <https://www.thoughtworks.com/insights/blog/reproducible-work-environments-using-docker>
        - `python/save-cache`: save pip packages to cache
      - `run`
        - for invoking command line programs
        - `command`: command to run via a non-login shell
        - `name`: (optional) title of the step to be shown in the CircleCI UI
  - `workflows`
    - for orchestrating jobs
    - `main`: unique name for a workflow
      - `jobs`: a list of jobs to run
        - `build-and-test`: a job name that exists in the `config.yml`
- To view the a pipeline's `config.yml`
  - on the CircleCI Pipelines page, `...` for one of the pipelines > View Config File
  - click 'Compiled' to see the effective configuration

### Customise `config.yml`

- `executor: python/default`
  - add `tag: 3.6.9` (or another specific Python Docker image tag listed on <https://circleci.com/docs/2.0/circleci-images/#python>)

```yml
executor: python/default
  tag: 3.6.9
```

- `command: ./manage.py test`
  - replace with `command: python -m unittest -v`

## Sources

- "Continuous Integration with Python and Circle CI." <https://scotch.io/tutorials/continuous-integration-with-python-and-circle-ci#toc-global-dependencies>.
- "Configuring CircleCI." <https://circleci.com/docs/2.0/configuration-reference/>
