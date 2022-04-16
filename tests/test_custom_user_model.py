import pytest
from django.contrib.auth import authenticate, get_user_model
from django.test import override_settings

pwd = "admin_pass"


@pytest.mark.django_db
class TestCustomUser:
    @staticmethod
    def create_user(**kwargs):
        user = get_user_model().objects.create(**kwargs)
        return user

    def test_regular_user_model_with_username(self, real_admin, real_user, rf):
        """test regular case, USERNAME_FIELD = username"""
        composed_username = "{} as {}".format(real_admin.username, real_user.username)
        authenticated_user = authenticate(
            request=rf, username=composed_username, password=pwd
        )
        assert authenticated_user == real_user

    @override_settings(AUTH_USER_MODEL="testapp.CustomUser1")
    def test_custom_user_model_with_email(self, rf):
        """test case custom model user, USERNAME_FIELD = email"""

        real_admin = self.create_user(
            username="custom1username",
            email="custom1admin@email.com",
            is_superuser=True,
        )
        real_admin.set_password(pwd)
        real_admin.save()

        real_user = self.create_user(
            username="custom1_real_test_user",
            email="custom1_real@mail.com",
        )
        real_user.set_password("user_pass")
        real_user.save()

        composed_username = "{} as {}".format(real_admin.email, real_user.email)
        authenticated_user = authenticate(
            request=rf, email=composed_username, password=pwd
        )
        assert authenticated_user == real_user

    @override_settings(AUTH_USER_MODEL="testapp.CustomUser2")
    def test_custom_user_model_with_user_identifier(self, rf):
        """test case custom model user, USERNAME_FIELD = user_identifier"""

        real_admin = self.create_user(
            username="custom2admin",
            user_identifier="custom2adminidentifier",
            email="custom2admin@email.com",
            is_superuser=True,
        )
        real_admin.set_password(pwd)
        real_admin.save()

        real_user = self.create_user(
            username="custom2user",
            user_identifier="custom2useridentifier",
            email="custom2_real@mail.com",
        )
        real_user.set_password("user_pass")
        real_user.save()

        composed_username = "{} as {}".format(
            real_admin.user_identifier, real_user.user_identifier
        )
        authenticated_user = authenticate(
            request=rf, user_identifier=composed_username, password=pwd
        )
        assert authenticated_user == real_user
