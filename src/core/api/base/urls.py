from django.urls import path
from . import notifications, breadcrumbs
from ...views.modals.open import open_modal_endpoint

# from . import modal

urlpatterns = [
    path(
        "modals/<str:modal_name>/retrieve",
        open_modal_endpoint,
        name="modal retrieve",
    ),
    path(
        "notifications/get",
        notifications.get_notification_html,
        name="notifications get",
    ),
    path("notifications/get_count", notifications.get_notification_count_html, name="notifications get count"),
    path(
        "notifications/delete/<int:id>",
        notifications.delete_notification,
        name="notifications delete",
    ),
    path("breadcrumbs/refetch/", breadcrumbs.update_breadcrumbs_endpoint, name="breadcrumbs refetch"),
]

app_name = "base"
