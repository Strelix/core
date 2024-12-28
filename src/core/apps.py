import importlib

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "core"
    verbose_name = "Strelix Core"

    DEFAULT_AUTHENTICATION_CLASSES = "core.api.public.authentication.CustomBearerAuthentication"

    def ready(self):
        from core.api.public.models import APIAuthToken
        import core.signals

        importlib.import_module("core.service.modals.modals")
        pass
