# Contributing

Contributions are very welcome. Tests can be run with [tox](https://tox.readthedocs.io/en/latest/), please ensure
the coverage at least stays the same before you submit a pull request.

## Local development

Install all the python interpreters you need via [pyenv](https://github.com/pyenv/pyenv). E.g.:

```bash
pyenv install 3.5.3
pyenv install 3.6.3
pyenv install 3.7.7
pyenv install 3.8.3
```
and then make them global with:

```bash
pyenv global 3.5.3 3.6.3 3.7.7 3.8.3
```

Clone the repo into a dir.
Create a virtualenv with the python system

```bash
tox --devenv venv
```

Activate the virtualenv 

```bash
. venv/bin/activate
```

Run the tests into the current virtualenv

```bash
pytest
```

or run the tests for all the environments defined into tox.ini

```bash
tox
```
