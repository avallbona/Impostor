# -*- coding: utf-8 -*-

import uuid
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models


class ImpostorLog(models.Model):
    impostor = models.ForeignKey(
        get_user_model(), verbose_name=_('Impostor'),
        related_name='impostor', db_index=True,
        on_delete=models.CASCADE
    )
    imposted_as = models.ForeignKey(
        get_user_model(), verbose_name=_('Logged in as'),
        related_name='imposted_as', db_index=True,
        on_delete=models.CASCADE
    )
    impostor_ip = models.GenericIPAddressField(
        verbose_name=_('Impostor\'s IP address'), null=True, blank=True
    )
    logged_in = models.DateTimeField(
        verbose_name=_('Logged on'), auto_now_add=True
    )
    # These last two will come into play with Django 1.3+, but are here now for easier migration
    logged_out = models.DateTimeField(
        verbose_name=_('Logged out'), null=True, blank=True
    )
    token = models.CharField(
        verbose_name=_('Token'), max_length=36, blank=True, db_index=True
    )

    def save(self, *args, **kwargs):
        """
        Custom save method

        :param args:
        :param kwargs:
        :return:
        """
        if not self.token and self.impostor:
            self.token = str(uuid.uuid4())

        super(ImpostorLog, self).save(*args, **kwargs)

    class Meta:
        """
        Description of the Meta Class.
        """

        verbose_name = _('Impostor log')
        verbose_name_plural = _('Impostor logs')
        ordering = ('-logged_in', 'impostor')

    def __str__(self):
        """
        str representation of the object.

        :return:
        """
        return '{} as {}'.format(self.impostor, self.imposted_as)
