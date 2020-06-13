# import datetime

import pytest
from django.contrib.auth import authenticate, get_user_model


from impostor.forms import BigAuthenticationForm
from impostor.models import ImpostorLog

admin_username = 'real_test_admin'
admin_pass = 'admin_pass'
admin_email = 'admin@email.com'

user_username = 'real_test_user'
user_email = 'real@mail.com'
user_pass = 'user_pass'

user_with_supergroup_pass = '1234qwer'


@pytest.mark.django_db
class TestImpostorLogin:

    def test_login_user(self):
        """
        checks that a regular user can login normally throught the next backend
        :return:
        """
        u = authenticate(username=user_username, password=user_pass)
        real_user = get_user_model().objects.get(username=user_username)
        assert u == real_user

    def test_login_admin(self):
        """
        checks that an admin user can login normally throught the next backend
        :return:
        """
        u = authenticate(username=admin_username, password=admin_pass)
        real_admin = get_user_model().objects.get(username=admin_username)
        assert u == real_admin

    def test_login_admin_as_user(self):
        """
        checks that an admin user can impersonate a regular user via impostor backend
        and that the login get reflected into the ImpostorLog table
        :return:
        """
        assert ImpostorLog.objects.count() == 0

        composed_username = '{} as {}'.format(admin_username, user_username)
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
        assert (entry.token and entry.token.strip() != "")

    def test_form(self):
        """
        test custom login form

        :return:
        """
        initial = {'username': user_username, 'password': user_pass}
        form = BigAuthenticationForm(data=initial)
        assert form.is_valid()
        assert form.cleaned_data['username'] == user_username
        assert form.cleaned_data['password'] == user_pass

        # Longer than contrib.auth default of 30 chars
        new_uname = '{} as {}'.format(admin_username, user_username)
        initial = {'username': new_uname, 'password': admin_pass}
        form = BigAuthenticationForm(data=initial)
        assert form.is_valid()
        assert form.cleaned_data['username'] == new_uname
        assert form.cleaned_data['password'] == admin_pass

        del initial['password']
        form = BigAuthenticationForm(data=initial)
        assert not form.is_valid()

    def test_login_admin_as_user_with_email(self):
        composed_username = '{} as {}'.format(admin_username, user_email)
        u = authenticate(username=composed_username, password=admin_pass)
        real_user = get_user_model().objects.get(email=user_email)
        assert u == real_user

    @pytest.mark.parametrize('first_user,password,impersonated_user,expected', [

        (pytest.lazy_fixture('real_admin'), admin_pass,
         pytest.lazy_fixture('real_user'), 'ok'),

        (pytest.lazy_fixture('real_admin'), admin_pass,
         pytest.lazy_fixture('real_admin'), 'ok'),

        (pytest.lazy_fixture('real_user'), user_pass,
         pytest.lazy_fixture('real_admin'), 'ko'),

        (pytest.lazy_fixture('real_user_with_supergroup'), user_with_supergroup_pass,
         pytest.lazy_fixture('real_user'), 'ok'),

        (pytest.lazy_fixture('real_user_with_supergroup'), user_with_supergroup_pass,
         pytest.lazy_fixture('real_admin'), 'ko'),

    ])
    def test_impersonation(self, first_user, password, impersonated_user, expected, custom_settings, rf):
        assert ImpostorLog.objects.count() == 0
        composed_username = '{} as {}'.format(first_user.username, impersonated_user.username)
        authenticated_user = authenticate(request=rf, username=composed_username, password=password)
        if expected == 'ok':
            assert authenticated_user == impersonated_user
            assert ImpostorLog.objects.count() == 1
            log = ImpostorLog.objects.first()
            assert log.impostor == first_user
            assert log.imposted_as == impersonated_user
        else:
            assert authenticated_user is None
