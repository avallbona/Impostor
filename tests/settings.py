DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        # 'NAME': 'test_db.sqlite',
    },
}

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "django.contrib.auth",
    "impostor",
    "tests.testapp",
]

AUTHENTICATION_BACKENDS = (
    "impostor.backend.AuthBackend",
    "django.contrib.auth.backends.ModelBackend",
)

MIDDLEWARE = []

USE_TZ = True

SECRET_KEY = "foobar"

LANGUAGE_CODE = "en-us"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    }
]


STATIC_URL = "/static/"

IMPOSTOR_GROUP = "impostor-group"
