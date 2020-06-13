# -*- coding: utf-8 -*-

from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.utils.translation import gettext_lazy as _


class BigAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=_("Username"), max_length=70)
