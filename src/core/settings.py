INSTALLED_APPS = ["django.contrib.auth", "django.contrib.contenttypes", "django.contrib.staticfiles", "core", "billing"]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
    "public_media": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {"location": "media/public", "base_url": "/media/public/"},
    },
    "private_media": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {"location": "media/private", "base_url": "/media/private/"},
    },
}

AUTH_USER_MODEL = "core.User"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
