# -*- coding: utf-8 -*-

import inspect

from django.contrib.auth.models import User, Group
from django.http import HttpRequest
from django.conf import settings

from .models import ImpostorLog


try:
    IMPOSTOR_GROUP = Group.objects.get(name=settings.IMPOSTOR_GROUP)
except (Group.DoesNotExist, AttributeError):
    IMPOSTOR_GROUP = None


def find_request():
    """
    Inspect running environment for request object. There should be one,
    but don't rely on it.
    """
    frame = inspect.currentframe()
    request = None
    f = frame

    while not request and f:
        if 'request' in f.f_locals and isinstance(f.f_locals['request'], HttpRequest):
            request = f.f_locals['request']
        f = f.f_back

    del frame
    return request


class AuthBackend:
    supports_anonymous_user = False
    supports_object_permissions = False
    supports_inactive_user = False

    def authenticate(self, request, username=None, password=None, *kwargs):
        auth_user = None
        try:
            # Admin logging as user?
            admin, uuser = [uname.strip() for uname in username.split(" as ")]

            # Check if admin exists and authenticates
            admin_obj = User.objects.get(username=admin)
            if (admin_obj.is_superuser or (IMPOSTOR_GROUP and IMPOSTOR_GROUP in admin_obj.groups.all())) \
                    and admin_obj.check_password(password):
                try:
                    auth_user = User.objects.get(username=uuser)
                except User.DoesNotExist:
                    auth_user = User.objects.get(email=uuser)

            if auth_user:
                # Superusers can only be impersonated by other superusers
                if auth_user.is_superuser and not admin_obj.is_superuser:
                    auth_user = None
                    raise Exception("Superuser can only be impersonated by a superuser.")

                # Try to find request object and maybe be lucky enough to find IP address there
                request = find_request()
                ip_addr = ''
                if request:
                    ip_addr = request.META.get('HTTP_X_FORWARDED_FOR',
                                               request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR', '')))
                    # if there are several ip addresses separated by comma
                    # like HTTP_X_FORWARDED_FOR returns,
                    # take only the first one, which is the client's address
                    if ',' in ip_addr:
                        ip_addr = ip_addr.split(',', 1)[0].strip()
                log_entry = ImpostorLog.objects.create(impostor=admin_obj, imposted_as=auth_user, impostor_ip=ip_addr)

                if log_entry.token and request:
                    request.session['impostor_token'] = log_entry.token

        except Exception:  # Nope. Do nothing and let other backends handle it.
            pass
        return auth_user

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
