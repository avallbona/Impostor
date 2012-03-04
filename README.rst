Impostor
========

Impostor is a Django application which allows staff members to login as
a different user by using their own username and password.

Every such authentication is recorded in database and listed in admin
interface to everyone with an access to ImpostorLog interface. However it is
not possible to delete log entries through admin interface to make covering
tracks more difficult.

Impostor was developed and tested with Django 1.2. It might work with
other versions too. It also depends on Django's authentication system and
assumes you use its usernames for authentication.

Impostor is a MMM project (http://mmm.si) developed by Marko Samastur
(markos@gaivo.net) licensed under MIT license.


Installation
------------
Impostor won't work, if you are not using Django's auth system. It currently
also assumes that you use username to identify your users and not something
else (like email).

First install impostor app files as you would any other Django app.
Next some changes to your Django settings file are in order. To
AUTHENTICATION_BACKENDS add:

    ``'impostor.backend.AuthBackend'``

This will add impostor auth backend to other backends. AUTHENTICATION_BACKENDS
is a tuple listing backends and if you don't have it yet, then add following
lines to your settings:
::

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'impostor.backend.AuthBackend',
    )

Also add 'impostor' app to INSTALLED_APPS.

Run 'python manage.py syncdb' to create needed table and you are set.


Usage
-----
By now you should have a working system. This means that your superuser users
(users with is_superuser flag set to True) can log in as different user by
using their password and following concatenation:

    ``staff_username as users_username``

Example: Let's say my username is markos and I want to login as user fry.
Then I would use 'markos as fry' as my username and my normal password for
password.

Every such log in is logged in ImpostorLog table that can be seen through
Django admin interface, but for obvious security reasons can't be
manipulated there.

You can widen set of users who can impose as other users by adding a setting
IMPOSTOR_GROUP to settings.py. Users belonging to a group with this name
will also be able to pretend to be somebody else (but not superusers).

Impostor also provides a replacement authentication form, because two
usernames can easily exceed 30 character limit of original form. Its name
is BigAuthenticationForm and you can find it in impostor.forms.

NOTE: Only superuser users can use this (you have to turn on is_superuser
for every user that needs this privilege) or those belonging to
IMPOSTOR_GROUP and every such log in gets recorded.

Also use IMPOSTOR_GROUP cautiously because it still allows impersonating
somebody with different set of permissions (and hence security breach).


TODO/Wishlist
-------------
- add support for log in with emails
- record when impostor logs out*
- mark "hijacked" requests (so impostor can tell when he is using website as
  somebody else and avoid doing something stupid or that you can limit what is
  doable in such case)
- framework for easy notification of hijacked users (so you can notify them
  that their account has been accessed if you wish)

[*] This feature depends on django auth signals coming in Django 1.3, which I am not using yet.


Known bugs
----------
- proper support for logging in with emails (currently broken)
