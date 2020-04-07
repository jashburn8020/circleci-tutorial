# CircleCI Tutorial

- [CircleCI Tutorial](#circleci-tutorial)
  - [Prerequisites](#prerequisites)
  - [Create small Python application](#create-small-python-application)
  - [Set up CircleCI](#set-up-circleci)
  - [The `config.yml` file](#the-configyml-file)
    - [Customise `config.yml`](#customise-configyml)
  - [Generate and save build and test artifacts](#generate-and-save-build-and-test-artifacts)
    - [Unit testing and code coverage](#unit-testing-and-code-coverage)
    - [Static analysis](#static-analysis)
    - [Configure CircleCI](#configure-circleci)
  - [Integrate with Codecov](#integrate-with-codecov)
  - [Sources](#sources)

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
- Write tests
  - [`test/test_maths.py`](test/test_maths.py)
- Run tests
  - `python -m unittest -v`
  - all the tests should fail
- Write implementation until the tests pass
  - [`src/maths.py`](src/maths.py)
- Generate requirements file
  - `pip freeze > requirements.txt`
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

## The `config.yml` file

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
        - uses `circleci/python:latest` Docker image, which [_should be avoided_](https://circleci.com/docs/2.0/executor-types/#docker-image-best-practices)
      - pre-built CircleCI Docker images: <https://circleci.com/docs/2.0/circleci-images/>
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
          - a virtual environment is not necessary on this step because the `python` orb already makes use of a Docker image
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
- To view the a pipeline's `config.yml` in CircleCI
  - on the CircleCI Pipelines page
    - `...` (for one of the pipelines) > View Config File
  - click 'Compiled' to see the effective configuration

### Customise `config.yml`

- `executor: python/default`
  - select a specific Python Docker image tag as listed on <https://circleci.com/docs/2.0/circleci-images/#python> (e.g., `3.6.9`)
  - replace with

```yml
executor:
  name: python/default
  tag: 3.6.9
```

- `command: ./manage.py test`
  - replace with `command: python -m unittest -v`
- Commit and push changes to GitHub
- This should trigger a successful build on CircleCI for this branch
- `config.yml` at this stage:

```yml
version: 2.1

orbs:
  python: circleci/python@0.2.1

jobs:
  build-and-test:
    executor:
      name: python/default
      tag: 3.6.9
    steps:
      - checkout
      - python/load-cache
      - python/install-deps
      - python/save-cache
      - run:
          command: python -m unittest -v
          name: Test

workflows:
  main:
    jobs:
      - build-and-test
```

## Generate and save build and test artifacts

### Unit testing and code coverage

- Enable JUnit XML reporting for `unittest`
  - install `unittest-xml-reporting`
    - `pip install unittest-xml-reporting`
  - test run
    - `python -m xmlrunner`
    - check that a file `TEST-test.test_maths.MathsTest-xxx.xml` containing test results is created
      - delete the file
- Enable unit test code coverage tracking using `coverage.py`
  - install `coverage`
    - `pip install coverage`
  - test run
    - `python -m coverage run -m unittest`
    - `python -m coverage report`

### Static analysis

- Enable code static analysis using `pylint`
  - install `pylint`
    - `pip install pylint`
  - generate `pylint` configuration file
    - `python -m pylint --generate-rcfile > .pylintrc`
  - install `pylint_junit`
    - to produce analysis report in JUnit XML format so that `pylint` messages can be viewed in CircleCI's test report
    - `pip install pylint_junit`
  - add `pylint_junit` as a plugin in `.pylintrc`
    - under `[MASTER]`: `load-plugins=pylint_junit`
  - test run
    - `python -m pylint --output-format=junit src`

### Configure CircleCI

- Regenerate `requirements.txt`
  - remember to remove `pkg-resources==0.0.0` if you're using Ubuntu
- Discard previous `run` step in `config.yml`, and update `steps` as follows:

```yaml
steps:
  - checkout
  - python/load-cache
  - python/install-deps
  - python/save-cache
  - run:
      command: |
        mkdir --parents test-results/unittest
        python -m xmlrunner --output test-results/unittest
      name: unittest
  - run:
      command: |
        mkdir artifacts
        python -m coverage run -m unittest
        python -m coverage report > artifacts/coverage.txt
      name: coverage.py
  - run:
      command: |
        mkdir --parents test-results/pylint
        # --exit-zero: pylint exits with non-zero unless the code is perfect
        python -m pylint --output-format=junit --exit-zero src > test-results/pylint/pylint.xml
      name: pylint
  - store_test_results:
      path: test-results
  - store_artifacts:
      path: test-results
  - store_artifacts:
      path: artifacts
```

- Commit changes and push to GitHub
- CircleCI will successfully build the latest changes
  - click on the completed build pipeline > 'build-and-test'
    - click on 'TESTS' to see `pylint` messages
    - click on 'ARTIFACTS' to see
      - `coverage.txt`
      - `pylint.xml`
      - `TEST-test.test_maths.MathsTest-xxx.xml`
- Note: you can choose to not use `pylint_junit`, and use `pylint`'s text output format
  - you will need up upload (store) the output as artifacts rather than test results

## Integrate with Codecov

## Sources

- "Continuous Integration with Python and Circle CI." <https://scotch.io/tutorials/continuous-integration-with-python-and-circle-ci#toc-global-dependencies>.
- "Configuring CircleCI." <https://circleci.com/docs/2.0/configuration-reference/>.
- "Collecting Test Metadata." <https://circleci.com/docs/2.0/collect-test-data/>.
- "Storing Build Artifacts." <https://circleci.com/docs/2.0/artifacts/>.
