from copy import copy


class CoreConfig:
    core_defaults = {"CORE_BILLING_ENABLED": False, "CORE_EXPIRY_MODELS": ["core.TeamInvitation", "core.PasswordSecret"]}

    django_defaults = {
        "DEFAULT_AUTO_FIELD": "django.db.models.BigAutoField",
        "SOCIAL_AUTH_USER_MODEL": "core.User",
        "AUTH_USER_MODEL": "core.User",
    }

    def _setup(self):
        from django.conf import settings

        options = {option: getattr(settings, option) for option in dir(settings) if option.startswith("CORE")}
        options.update(self.django_defaults)
        self.attrs = copy(self.core_defaults)
        self.attrs.update(options)

    def __init__(self):
        self._setup()

    def __getattr__(self, item):
        return self.attrs.get(item, None)

    def __setattribute__(self, key, value):
        self.attrs[key] = value
