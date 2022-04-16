import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import ImpostorLog

log = logging.getLogger(__name__)


class ImpostorException(Exception):
    pass


class AuthBackend:
    supports_anonymous_user = False
    supports_object_permissions = False
    supports_inactive_user = False
    separator = " as "

    @property
    def impostor_group(self):
        try:
            imp_group, __ = Group.objects.get_or_create(name=settings.IMPOSTOR_GROUP)
        except (Group.DoesNotExist, AttributeError):
            imp_group = None
        return imp_group

    def user_in_impostor_group(self, user):
        """
        check is the user is in the impostor group

        :param user:
        :return:
        """
        return self.impostor_group and self.impostor_group in user.groups.all()

    @staticmethod
    def ip_address(request):
        """
        try to obtain the ip address from request

        :param request:
        :return:
        """
        try:
            ip_addr = request.META.get(
                "HTTP_X_FORWARDED_FOR",
                request.META.get("HTTP_X_REAL_IP", request.META.get("REMOTE_ADDR", "")),
            )
        except AttributeError:
            ip_addr = ""
        # if there are several ip addresses separated by comma like HTTP_X_FORWARDED_FOR returns,
        # take only the first one, which is the client's address
        if "," in ip_addr:
            ip_addr = ip_addr.split(",", 1)[0].strip()
        return ip_addr

    def is_user_allowed_to_impersonate(self, adm_obj):
        """
        verifies is the user who wants to impersonate another user can do it

        :param adm_obj:
        :return:
        """
        return adm_obj.is_superuser or self.user_in_impostor_group(adm_obj)

    @staticmethod
    def save_impostor_token_into_session(log_entry, request):
        """
        tries to save the impostor token into session

        :param log_entry:
        :param request:
        :return:
        """
        if not log_entry.token or not request:
            return
        try:
            request.session["impostor_token"] = log_entry.token
        except Exception as e:
            log.info(msg=str(e))

    def authenticate(self, request, username=None, password=None, **kwargs):
        auth_user = None
        User = get_user_model()

        try:
            if not username:
                username = kwargs.get(User.USERNAME_FIELD)
            if username is None or password is None:
                raise ImpostorException(
                    _("Both USERNAME_FIELD and password is required")
                )
            # if the split does not generate the admin and uuser
            # raise and exception and continues with the following backend
            try:
                admin, uuser = [
                    uname.strip() for uname in username.split(self.separator)
                ]
            except ValueError:
                raise ImpostorException(_("Regular login, moving to next auth backend"))

            # Check if admin exists, authenticates and is
            # allowed to impersonate another user
            try:
                adm_obj = User._default_manager.get_by_natural_key(admin)
            except User.DoesNotExist:
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a nonexistent user.
                # (see https://code.djangoproject.com/ticket/20760)
                User().set_password(password)
                raise ImpostorException(_("Admin user is not active"))

            if self.is_user_allowed_to_impersonate(adm_obj) and adm_obj.check_password(
                password
            ):
                # get the user we want to impersonate
                try:
                    auth_user = User._default_manager.get_by_natural_key(uuser)
                except User.DoesNotExist:
                    # default password hasher is not required to run since user
                    # password is not checked
                    raise ImpostorException(_("User is not active"))

                # Superusers can only be impersonated by other superusers
                if auth_user.is_superuser and not adm_obj.is_superuser:
                    auth_user = None
                    raise ImpostorException(
                        _("Superuser can only be impersonated by a superuser.")
                    )

                # creates the impostor log entry
                log_entry = ImpostorLog.objects.create(
                    impostor=adm_obj,
                    imposted_as=auth_user,
                    impostor_ip=self.ip_address(request),
                )

                # save impostor_token into the session
                self.save_impostor_token_into_session(log_entry, request)

        except Exception as e:  # Nope. Do nothing and let other backends handle it.
            log.info(msg=str(e))
        return auth_user

    @staticmethod
    def get_user(user_id):
        User = get_user_model()
        try:
            return User._default_manager.get(pk=user_id)
        except User.DoesNotExist:
            pass
