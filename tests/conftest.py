import os

import django
import pytest
from django.contrib.auth import get_user_model


def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    django.setup()


admin_username = "real_test_admin"
admin_email = "admin@email.com"
admin_pass = "admin_pass"

user_username = "real_test_user"
user_email = "real@mail.com"
user_pass = "user_pass"

user_with_supergroup_pass = "1234qwer"


@pytest.fixture(autouse=True)
def custom_settings(settings):
    settings.IMPOSTOR_GROUP = "impostor-group"
    return settings


@pytest.fixture(autouse=True)
def real_admin():
    real_admin = get_user_model().objects.create(
        username=admin_username,
        email=admin_email,
        password=admin_pass,
    )
    real_admin.is_superuser = True
    real_admin.set_password(admin_pass)
    real_admin.save()
    return real_admin


@pytest.fixture(autouse=True)
def real_user():
    real_user = get_user_model().objects.create(
        username=user_username, email=user_email, password=user_pass
    )
    real_user.set_password(user_pass)
    real_user.save()
    return real_user


@pytest.fixture()
def real_user_with_supergroup(custom_settings):
    user, __ = get_user_model().objects.get_or_create(
        username="user-with-supergroup",
        email="user.with.supergroup@email.com",
        password="1234qwer",
    )
    user.set_password(user_with_supergroup_pass)
    user.save()

    from django.contrib.auth.models import Group

    impostor_group, __ = Group.objects.get_or_create(
        name=custom_settings.IMPOSTOR_GROUP
    )
    user.groups.add(impostor_group)
    return user
