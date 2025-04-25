# Change Log

## 3.2.0 (2025-04-26)
  * added support for django 5.0, 5.1 and 5.2
  * added support for python 3.13
  * dropped support for django 2.0, 2.1, 2.2, 3.0 and 3.1
  * dropped support for python 3.7
  * removed default_app_config variable from __init__.py
  * refactored tests to remove pytest-lazy-fixture plugin (which is not mantained anymore)

## 3.1.0 (2023-12-03)
  * added support for django 4.1 and 4.2
  * added support for python 3.10, 3.11 and 3.12
  * dropped support for django 1.11
  * dropped support for python 3.4, 3.5 and 3.6

## 3.0.0 (2022-04-15)
  * added support for django 3.2 and django 4.0
  * implemented support for custom user model and custom USERNAME_FIELD ([Saurav Sharma](https://github.com/iamsauravsharma))
  * added pre-commit config file
  * applied black and isort to source code

## 2.0.5 (2021-03-29)

  * added support for django 3.1
  * added support for python 3.9
  * updated dev dependencies
  * updated documentation
  * added code of conduct
  * added contributing
  * added django versions badge

## 2.0.4 (2020-06-21)

  * Refactored setup.py in order to pack all the needed files
  * Extended the default admin templeta to show `user logged as another user`
  * Added `__str__` to ImpostorLog
  * Updated MANIFEST.in
  * Moved some package metadata to `__init__`
  * Improved code coverage

## 2.0.3 (2020-06-20)

  * Adjusted github action for tests
  * Improved some documentation

## 2.0.2 (2020-06-17)

  * Fixed some code style issues
  * Changed token generation in ImpostorLog
  * Added Codacy badge

## 2.0.1 (2020-06-14)

  * Added codecov coverage
  * Improved code coverage
  * Fixed test execution with django versions

## 2.0.0 (2020-06-13)

  * Added informative badges on README.md
  * Adapted Impostor to newer versions of django 1.11, 2.0, 2.1, 2.2, 3.0
  * Added tox for test running in diferent python and django versions
  * Tests migrated to pytest
  * Improved tests and coverage
  * Added publishing to pypi.org via github action
  * Added support for django custom_user_model
  * updated todo list
  * Improved documentation on README.md
  * Added changelog
  * Removed unnecessary code
  * Added migrations
  * Added flake8 linter
