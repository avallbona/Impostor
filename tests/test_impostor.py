import pytest
from django.contrib.auth import authenticate, get_user_model

from impostor.backend import AuthBackend
from impostor.forms import BigAuthenticationForm
from impostor.models import ImpostorLog
from impostor.templatetags.impostor_tags import get_impersonated_as

admin_username = "real_test_admin"
admin_pass = "admin_pass"
admin_email = "admin@email.com"

user_username = "real_test_user"
user_email = "real@mail.com"
user_pass = "user_pass"

user_with_supergroup_pass = "1234qwer"

fake_admin_username = "fake_test_admin"
fake_user_username = "fake_test_user"


@pytest.mark.django_db
class TestImpostorLogin:
    def test_login_user(self):
        """checks that a regular user can login normally through the next backend"""
        u = authenticate(username=user_username, password=user_pass)
        real_user = get_user_model().objects.get(username=user_username)
        assert u == real_user

    def test_login_admin(self):
        """checks that an admin user can login normally through the next backend"""
        u = authenticate(username=admin_username, password=admin_pass)
        real_admin = get_user_model().objects.get(username=admin_username)
        assert u == real_admin

    def test_login_admin_as_user(self):
        """checks that an admin user can impersonate a regular user via
        impostor backend and that the login get reflected into the
        ImpostorLog table"""
        assert ImpostorLog.objects.count() == 0

        composed_username = "{} as {}".format(admin_username, user_username)
        u = authenticate(username=composed_username, password=admin_pass)
        real_user = get_user_model().objects.get(username=user_username)
        assert u == real_user

        # Check if logs contain an entry now
        logs_entries = ImpostorLog.objects.all()
        assert len(logs_entries) == 1

        entry = logs_entries[0]
        # today = datetime.date.today()
        # lin = entry.logged_in
        assert entry.impostor.username == admin_username
        assert entry.imposted_as.username == user_username

        # assert (lin.year == today.year and lin.month == today.month and lin.day == today.day)
        assert entry.token and entry.token.strip() != ""

    def test_missing_authenticate_field(self):
        """checks that user cannot login if user USERNAME_FIELD/username
        or password field is missing"""
        composed_username = "{} as {}".format(admin_username, user_username)
        user = authenticate(
            random_username_field=composed_username, password=admin_pass
        )
        assert user is None

    def test_user_is_not_returned_if_admin_user_not_found(self):
        """checks that admin user doesn't exist case are properly
        handled out by backend"""
        composed_username = "{} as {}".format(fake_admin_username, user_username)
        user = authenticate(username=composed_username, password=admin_pass)
        assert user is None

    def test_user_is_not_returned_if_user_not_found(self):
        """checks that normal user doesn't exist case are properly
        handled out by backend"""
        composed_username = "{} as {}".format(admin_username, fake_user_username)
        user = authenticate(username=composed_username, password=admin_pass)
        assert user is None

    def test_form(self):
        """test custom login form"""
        initial = {"username": user_username, "password": user_pass}
        form = BigAuthenticationForm(data=initial)
        assert form.is_valid()
        assert form.cleaned_data["username"] == user_username
        assert form.cleaned_data["password"] == user_pass

        # Longer than contrib.auth default of 30 chars
        new_uname = "{} as {}".format(admin_username, user_username)
        initial = {"username": new_uname, "password": admin_pass}
        form = BigAuthenticationForm(data=initial)
        assert form.is_valid()
        assert form.cleaned_data["username"] == new_uname
        assert form.cleaned_data["password"] == admin_pass

        del initial["password"]
        form = BigAuthenticationForm(data=initial)
        assert not form.is_valid()

    @pytest.mark.parametrize(
        "first_user,password,impersonated_user,expected",
        [
            (
                "real_admin",
                admin_pass,
                "real_user",
                "ok",
            ),
            (
                "real_admin",
                admin_pass,
                "real_admin",
                "ok",
            ),
            (
                "real_user",
                user_pass,
                "real_admin",
                "ko",
            ),
            (
                "real_user_with_supergroup",
                user_with_supergroup_pass,
                "real_user",
                "ok",
            ),
            (
                "real_user_with_supergroup",
                user_with_supergroup_pass,
                "real_admin",
                "ko",
            ),
        ],
    )
    def test_impersonation(
        self,
        request,
        first_user,
        password,
        impersonated_user,
        expected,
        custom_settings,
        rf,
    ):
        """
        check different use cases of impersonation

        :param first_user:
        :param password:
        :param impersonated_user:
        :param expected:
        :param custom_settings:
        :param rf:
        :return:
        """
        first_user = request.getfixturevalue(first_user)
        impersonated_user = request.getfixturevalue(impersonated_user)

        setattr(rf, "META", {})
        rf.META["HTTP_X_FORWARDED_FOR"] = "127.0.0.1,192.168.0.1"
        assert ImpostorLog.objects.count() == 0
        composed_username = "{} as {}".format(
            first_user.username, impersonated_user.username
        )
        authenticated_user = authenticate(
            request=rf, username=composed_username, password=password
        )
        if expected == "ok":
            assert authenticated_user == impersonated_user
            assert ImpostorLog.objects.count() == 1
            log = ImpostorLog.objects.first()
            assert log.impostor == first_user
            assert log.imposted_as == impersonated_user
            assert log.impostor_ip == "127.0.0.1"
        else:
            assert authenticated_user is None

    @pytest.mark.parametrize(
        "user_passed, user_expected",
        [
            (
                "real_user_with_supergroup",
                "real_user_with_supergroup",
            ),
            (None, None),
        ],
    )
    def test_get_user(self, request, user_passed, user_expected):
        """
        check get_user method
        :param user_passed:
        :param user_expected:
        :return:
        """
        user_passed = request.getfixturevalue(user_passed) if user_passed else None
        user_expected = (
            request.getfixturevalue(user_expected) if user_expected else None
        )

        try:
            user_id = user_passed.id
        except AttributeError:
            user_id = None
        result = AuthBackend.get_user(user_id)
        assert result == user_expected

    @pytest.mark.parametrize("existing_attr", [True, False])
    def test_impostor_group(self, custom_settings, existing_attr):
        """
        check impostor_group property
        :param custom_settings:
        :return:
        """
        if existing_attr:
            delattr(custom_settings, "IMPOSTOR_GROUP")
            assert AuthBackend().impostor_group is None
        else:
            assert AuthBackend().impostor_group is not None

    @pytest.mark.parametrize("in_session,expected", [(True, True), (False, False)])
    def test_impersonated_as_tag(self, real_admin, real_user, rf, in_session, expected):
        obj = ImpostorLog.objects.create(impostor=real_admin, imposted_as=real_user)
        setattr(rf, "session", {})
        if in_session:
            rf.session["impostor_token"] = obj.token
        result = get_impersonated_as(rf)
        if expected:
            assert result == obj
        else:
            assert result != obj

    def test_impostor_log_str(self, real_admin, real_user):
        obj = ImpostorLog.objects.create(impostor=real_admin, imposted_as=real_user)
        assert str(obj) == "{} as {}".format(real_admin.username, real_user.username)
