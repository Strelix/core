import os
from typing import Dict, List

from django.conf import settings


class CoreConfig:
    BILLING_ENABLED: bool = False
    EXPIRY_MODELS: List[str] = [
        "core.TeamInvitation",
        "core.PasswordSecret",
    ]
    SETTINGS_PAGE_CONTEXT_HANDLERS: Dict[str, str] = {
        "account": "core.service.settings.view.get_account_page_context",
        "api_keys": "core.service.settings.view.api_keys_page_context",
        "account_defaults": "core.service.settings.view.account_defaults_context",
        "profile": "core.service.settings.view.profile_context",
        "account_security": "core.service.settings.view.account_security_context",
    }

    # DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"
    # SOCIAL_AUTH_USER_MODEL: str = "core.User"
    # AUTH_USER_MODEL: str = "core.User"
    # LOGGING: Dict[str, Dict] = {
    #     "version": 1,
    #     "disable_existing_loggers": False,
    #     "handlers": {
    #         "console": {
    #             "level": "DEBUG",
    #             "class": "logging.StreamHandler",
    #         },
    #     },
    #     "loggers": {
    #         "django": {
    #             "handlers": ["console"],
    #             "level": "DEBUG",
    #             "propagate": True,
    #         },
    #         "django.request": {
    #             "handlers": ["console"],
    #             "level": "ERROR",
    #             "propagate": False,
    #         },
    #     },
    # }

    def __init__(self):
        self._setup()

    def _setup(self):
        from django.conf import settings

        django_settings_options = {option[5:]: getattr(settings, option) for option in dir(settings) if option.startswith("CORE_")}
        environ_options = {key: value for key, value in os.environ.items() if key.startswith("CORE_")}

        for key, value in {**django_settings_options, **environ_options}.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __getattr__(self, item: str):
        raise AttributeError(f"'CoreConfig' object has no attribute '{item}'")
