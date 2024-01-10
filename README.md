# Impostor

[![pypi](https://img.shields.io/pypi/v/impostor.svg)](https://pypi.python.org/pypi/impostor/)
[![codecov](https://codecov.io/gh/avallbona/Impostor/branch/master/graph/badge.svg)](https://codecov.io/gh/avallbona/Impostor)
[![Downloads](https://pepy.tech/badge/impostor)](https://pepy.tech/project/impostor)
[![Hit counter](http://hits.dwyl.com/avallbona/impostor.svg)](http://hits.dwyl.com/avallbona/impostor)
[![Python versions](https://img.shields.io/pypi/pyversions/impostor.svg)](https://pypi.org/project/Impostor/)
![PyPI - Django Version](https://img.shields.io/pypi/djversions/impostor)
![Python package](https://github.com/avallbona/Impostor/workflows/python%20package/badge.svg?branch=master)
![Upload Python Package](https://github.com/avallbona/Impostor/workflows/Upload%20Python%20Package/badge.svg?branch=master)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/98d1f4b3225046e1aa839813b47bb44f)](https://www.codacy.com/manual/avallbona/Impostor?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=avallbona/Impostor&amp;utm_campaign=Badge_Grade)

Impostor is a Django application which allows staff members to login as
a different user by using their own username and password.

**Login**

![`Login`](https://i.imgur.com/TaoZyOh.png)

**Logged as**

![`Logged as`](https://i.imgur.com/db3fSi8.png)

**Impostor log**

![`Impostor log`](https://i.imgur.com/OQ9IWB7.png)

Every such authentication is recorded in database and listed in admin
interface to everyone with an access to ImpostorLog interface. However it is
not possible to delete log entries through admin interface to make covering
tracks more difficult.

Impostor was tested with Django 1.11 and above. It might work with
other versions too. It also depends on Django's authentication system and
assumes you use its usernames for authentication.

Impostor is a [MMM](http://mmm.si) project  developed by Marko Samastur
(markos@gaivo.net) and maintained by Andreu Vallbona (avallbona@gmail.com)  
licensed under MIT license.

## Installation

Impostor won't work, if you are not using Django's auth system. It currently
uses settings AUTH_USER_MODEL(default: `django.contrib.auth.models.User`)
USERNAME_FIELD(default: `username`) or username as authentication parameter
along with password and user object _default_manager get_by_natural_key
function for returning user object from USERNAME_FIELD.

First install impostor app files as you would any other Django app

```bash
pip install impostor
```

Next some changes to your Django settings file are inorder.

Add `impostor.backend.AuthBackend` To **AUTHENTICATION_BACKENDS** :
This will add impostor auth backend to other backends. **AUTHENTICATION_BACKENDS**
is a tuple listing backends and if you don't have it yet, then add following
lines to your settings:

```python
AUTHENTICATION_BACKENDS = (
    'impostor.backend.AuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)
```

Also add `impostor` app to INSTALLED_APPS.

```python
INSTALLED_APPS = [
    '...', 
    'impostor',
]
```

In order to be able to see the `user logged as anotheruser` in the django admin,
be sure to include the 'impostor' app before the 'django.contrib.admin' in the **INSTALLED_APPS**.

Run

```bash
python manage.py migrate
```

to create needed table and you are set.

## Usage

By now you should have a working system. This means that your superuser users
(users with is_superuser flag set to True) can log in as different user by
using their password and following concatenation:

```bash
staff_username as users_username
```

Example: Let's say my username is markos and I want to login as user fry.
Then I would use '**markos as fry**' as my username and my normal password for
password.

Every such log in is logged in **ImpostorLog** table that can be seen through
Django admin interface, but for obvious security reasons can't be
manipulated there.

You can widen set of users who can impose as other users by adding a setting
**IMPOSTOR_GROUP** to settings.py. Users belonging to a group with this name
will also be able to pretend to be somebody else (but not superusers).

Impostor also provides a replacement authentication form, because two
usernames can easily exceed 30 character limit of original form. Its name
is **BigAuthenticationForm** and you can find it in impostor.forms.

NOTE: Only superuser users can use this (you have to turn on is_superuser
for every user that needs this privilege) or those belonging to
IMPOSTOR_GROUP and every such log in gets recorded.

Also use IMPOSTOR_GROUP cautiously because it still allows impersonating
somebody with different set of permissions (and hence security breach).

## Contributing

Contributions are very welcome. Tests can be run with [tox](https://tox.readthedocs.io/en/latest/), please ensure
the coverage at least stays the same before you submit a pull request.

## Local development

Install all the python interpreters you need via [pyenv](https://github.com/pyenv/pyenv). E.g.:

```bash
pyenv install 3.9.2
pyenv install 3.8.8
pyenv install 3.7.7
pyenv install 3.6.13
pyenv install 3.5.3
```

and then make them global with:

```bash
pyenv global 3.9.2 3.8.8 3.7.7 3.6.13 3.5.3 
```

Run the tests

```bash
tox
```

## Issues

If you encounter any problems, please [file an issue](https://github.com/avallbona/impostor/issues) along with a detailed description.

## TODO/Wishlist

  * record when impostor logs out
  * mark "hijacked" requests (so impostor can tell when he is using website as
    somebody else and avoid doing something stupid or that you can limit what is
    doable in such case)
  * framework for easy notification of hijacked users (so you can notify them
    that their account has been accessed if you wish)
  * add some tests to improve the coverage
