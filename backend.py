import django.contrib.auth as auth
from django.contrib.auth.models import User
from models import ImpostorLog

class AuthBackend:
	supports_anonymous_user = False
	supports_object_permissions = False
	supports_inactive_user = False

	def authenticate(self, username=None, password=None):
		auth_user = None
		try:
			# Admin logging as user?
			admin, uuser = [ uname.strip() for uname in username.split(" as ") ]

			# Check if admin exists and authenticates
			admin_obj = User.objects.get(username=admin)
			if admin_obj.is_staff and admin_obj.check_password(password):
				auth_user = User.objects.get(username=uuser)

			if auth_user:
				log_entry = ImpostorLog.objects.create(impostor=admin_obj, imposted_as=auth_user)
				'''
				if log_entry.token:
					auth_user.impostor_token = log_entry.token
				'''

		except:
			# Nah, just user. Do nothing and let other backends handle it.
			pass
		return auth_user

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None
