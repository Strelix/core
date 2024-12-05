from django.urls import path

from core.api.maintenance.now import handle_maintenance_now_endpoint

urlpatterns = [
    path("cleanup/", handle_maintenance_now_endpoint, name="cleanup"),
]

app_name = "maintenance"
