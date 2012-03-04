from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from models import ImpostorLog
from forms import BigAuthenticationForm
import datetime

admin_username = 'real_test_admin'
admin_pass = 'admin_pass'
user_username = 'real_test_user'
user_email = 'real@mail.com'
user_pass = 'user_pass'

class TestImpostorLogin(TestCase):
	def setUp(self):
		real_admin = User.objects.create(username=admin_username, password=admin_pass)
		real_admin.is_superuser = True
		real_admin.set_password(admin_pass)
		real_admin.save()

		real_user = User.objects.create(username=user_username, email=user_email, password=user_pass)
		real_user.set_password(user_pass)
		real_user.save()


	def test_login_user(self):
		u = authenticate(username=user_username, password=user_pass)
		real_user = User.objects.get(username=user_username)

		self.failUnlessEqual(u, real_user)

	def test_login_user_with_email(self):
		u = authenticate(email=user_email, password=user_pass)
		real_user = User.objects.get(email=user_email)

		self.failUnlessEqual(u, real_user)

	def test_login_admin(self):
		u = authenticate(username=admin_username, password=admin_pass)
		real_admin = User.objects.get(username=admin_username)

		self.failUnlessEqual(u, real_admin)


	def test_login_admin_as_user(self):
		no_logs_entries = len(ImpostorLog.objects.all())
		self.failUnlessEqual(no_logs_entries, 0)

		u = authenticate(username="%s as %s" % (admin_username, user_username), password=admin_pass)
		real_user = User.objects.get(username=user_username)

		self.failUnlessEqual(u, real_user)

		# Check if logs contain an entry now
		logs_entries = ImpostorLog.objects.all()
		self.failUnlessEqual(len(logs_entries), 1)

		entry = logs_entries[0]
		today = datetime.date.today()
		lin = entry.logged_in
		self.failUnlessEqual(entry.impostor.username, admin_username)
		self.failUnlessEqual(entry.imposted_as.username, user_username)
		self.assertTrue(lin.year == today.year and lin.month == today.month and lin.day == today.day)
		self.assertTrue(entry.token and entry.token.strip() != "")


	def test_form(self):
		initial = { 'username': user_username, 'password': user_pass}
		form = BigAuthenticationForm(data=initial)
		self.assertTrue(form.is_valid())
		self.failUnlessEqual(form.cleaned_data['username'], user_username)
		self.failUnlessEqual(form.cleaned_data['password'], user_pass)

		new_uname = "%s as %s" % (admin_username, user_username) # Longer than contrib.auth default of 30 chars
		initial = { 'username': new_uname, 'password': admin_pass }
		form = BigAuthenticationForm(data=initial)
		self.assertTrue(form.is_valid())
		self.failUnlessEqual(form.cleaned_data['username'], new_uname)
		self.failUnlessEqual(form.cleaned_data['password'], admin_pass)

		del initial['password']
		form = BigAuthenticationForm(data=initial)
		self.assertFalse(form.is_valid())
