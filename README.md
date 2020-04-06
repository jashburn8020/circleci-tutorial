# CircleCI Tutorial

## Prerequisites

- [GitHub](https://github.com/) account
  - create a public repository for this tutorial, e.g., `circleci-tutorial`
  - clone the repository, and use it as your project directory
- [CircleCI](https://circleci.com/) account
  - sign up to CircleCI using your GitHub account
- [Codecov](https://codecov.io/) account

## Create small Python application

- Create and checkout a branch in your Git repository
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
-

## Sources

- "Continuous Integration with Python and Circle CI." <https://scotch.io/tutorials/continuous-integration-with-python-and-circle-ci#toc-global-dependencies>.
