from django.apps import AppConfig


class TestAppConfig(AppConfig):
    name = "testapp"
    verbose_name = "Test app"
    default_auto_field = "django.db.models.AutoField"
