# CircleCI Tutorial

## Prerequisites

- [GitHub](https://github.com/) account
  - create a public repository for this tutorial, e.g., `circleci-tutorial`
  - clone the repository, and use it as your project directory
- [CircleCI](https://circleci.com/) account
  - sign up to CircleCI using your GitHub account
- [Codecov](https://codecov.io/) account

## Create small Python application

- Create a virtual environment
  - `python3 -m venv venv`
  - `source venv/bin/activate`
- Install additional modules
  - coverage
- Write tests
  - [test/test_maths.py](test/test_maths.py)
- Run tests
  - `python -m unittest -v`
  - all the tests should fail
- Write implementation until the tests pass
  - [src/maths.py](src/maths.py)
- Run `coverage`
  - `coverage run -m unittest`
  - `coverage report`
- Generate requirements file
  - `pip freeze > requirements.txt`
  - see [requirements.txt](requirements.txt)

## Sources

- "Continuous Integration with Python and Circle CI." <https://scotch.io/tutorials/continuous-integration-with-python-and-circle-ci#toc-global-dependencies>.
