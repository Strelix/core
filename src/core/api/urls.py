from __future__ import annotations

from django.urls import include
from django.urls import path

urlpatterns = [
    path("base/", include("core.api.base.urls")),
    path("teams/", include("core.api.teams.urls")),
    path("settings/", include("core.api.settings.urls")),
    path("quotas/", include("core.api.quotas.urls")),
    # path("clients/", include("backend_utils.clients.api.urls")),
    path("emails/", include("core.api.emails.urls")),
    path("maintenance/", include("core.api.maintenance.urls")),
    path("landing_page/", include("core.api.landing_page.urls")),
    path("public/", include("core.api.public.urls")),
    #     path("", include("backend_utils.finance.api.urls")),
]

app_name = "api"
