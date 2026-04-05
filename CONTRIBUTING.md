# Contributing

Contributions are very welcome. Tests can be run with [tox](https://tox.readthedocs.io/en/latest/), please ensure
the coverage at least stays the same before you submit a pull request.

## Local development

Install all the python interpreters you need via [pyenv](https://github.com/pyenv/pyenv). E.g.:

```bash
pyenv install 3.14.3
pyenv install 3.13.2
pyenv install 3.12.2
pyenv install 3.11.8
pyenv install 3.10.13
pyenv install 3.9.2
pyenv install 3.8.8
```
and then make them global with:

```bash
pyenv global 3.14.3 3.13.2 3.12.2 3.11.8 3.10.13 3.9.2 3.8.8 
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
