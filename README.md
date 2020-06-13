# Impostor

[![pypi](https://img.shields.io/pypi/v/impostor.svg)](https://pypi.python.org/pypi/impostor/)
[![Downloads](https://pepy.tech/badge/impostor)](https://pepy.tech/project/impostor)
[![See Build Status on Travis CI](https://travis-ci.org/avallbona/impostor.svg?branch=master)](https://travis-ci.org/avallbona/impostor)
[![Hit counter](http://hits.dwyl.com/avallbona/impostor.svg)](http://hits.dwyl.com/avallbona/impostor)
[![Python versions](https://img.shields.io/pypi/pyversions/impostor.svg)](https://pypi.org/project/Impostor/)

Impostor is a Django application which allows staff members to login as
a different user by using their own username and password.

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
also assumes that you use username to identify your users and not something
else (like email).

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

Run

```bash
python manage.py migrate
```

to create needed table and you are set.

## Usage

By now you should have a working system. This means that your superuser users
(users with is_superuser flag set to True) can log in as different user by
using their password and following concatenation:

```
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


## TODO/Wishlist

* add support for log in with emails
* record when impostor logs out
* mark "hijacked" requests (so impostor can tell when he is using website as
  somebody else and avoid doing something stupid or that you can limit what is
  doable in such case)
* framework for easy notification of hijacked users (so you can notify them
  that their account has been accessed if you wish)
* improve the package description page
* add changelog
* add some tests to improve the coverage
* add pypy version badge
* add travis.ci to run the tests
* add github action to run the tests
* add github action to publish the package on pypi
* add test execution on travis

### Known bugs

* proper support for logging in with emails (currently broken)
