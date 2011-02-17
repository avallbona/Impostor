from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.utils.translation import ugettext_lazy as _

class BigAuthenticationForm(AuthenticationForm):
	username = forms.CharField(label=_("Username"), max_length=70)
