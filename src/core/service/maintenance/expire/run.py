from datetime import timedelta
from typing import Type, Optional, List

from django.conf import settings
from django.db import models
from django.db.models import QuerySet

from django.apps import apps

from django.utils import timezone

"""
Every model MUST have the field "expires" as:

expires = models.DateTimeField(null=True, blank=True)
"""


def expire_models_task():
    return expire_and_cleanup_objects(getattr(settings, "EXPIRY_MODELS", None))


def expire_and_cleanup_objects(model_list: Optional[List[str]] = None) -> str:
    if model_list is None:
        model_list = ["core.TeamInvitation", "core.PasswordSecret"]

    deactivated_items: int = 0
    deleted_items: int = 0

    now = timezone.now()

    for model in model_list:
        app_label, model_name = model.split(".")

        model_cls = apps.get_model(app_label=app_label, model_name=model_name)

        # Delete objects that have been inactive and expired for more than 14 days
        over_14_days_expired = model_cls.all_objects.filter(expires__lte=now - timedelta(days=14))  # type: ignore[attr-defined]
        deleted_items += over_14_days_expired.count()
        over_14_days_expired.delete()

        # Deactivate expired items that got missed
        to_deactivate: QuerySet[models.Model] = model_cls.all_objects.filter(expires__lte=now, active=True)  # type: ignore[attr-defined]

        deactivated_items += to_deactivate.count()
        to_deactivate.update(active=False)

    return f"Deactivated {deactivated_items} objects and deleted {deleted_items} objects."
