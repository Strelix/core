import importlib

from django.apps import AppConfig
from django.conf import settings


class BillingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "billing"

    def ready(self):
        from . import signals

        self._load_project_signals()

    def _load_project_signals(self):
        for app_name in getattr(settings, "INSTALLED_APPS", []):
            try:
                module_name = f"{app_name}.billing.signals"
                importlib.import_module(module_name)
            except ModuleNotFoundError:
                pass
