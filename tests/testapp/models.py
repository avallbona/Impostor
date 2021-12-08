from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser1(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    user_identifier = models.CharField(max_length=100)

    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get "
        "all permissions granted to each of their groups.",
        related_name="custom1_user_set",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="custom1_user_set",
    )

    class Meta:
        verbose_name = "Custom user 1"


class CustomUser2(AbstractUser):
    USERNAME_FIELD = "user_identifier"
    REQUIRED_FIELDS = ["user_identifier"]

    user_identifier = models.CharField(max_length=100)

    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get "
        "all permissions granted to each of their groups.",
        related_name="custom2_user_set",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="custom2_user_set",
    )

    class Meta:
        verbose_name = "Custom user 2"
