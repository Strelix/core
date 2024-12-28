from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.urls import path
from django.urls import re_path as url
from django.views.generic import RedirectView
from django.views.static import serve

from core.api.public.swagger_ui import get_swagger_ui, get_swagger_endpoints

url(
    r"^frontend/static/(?P<path>.*)$",
    serve,
    {"document_root": settings.STATICFILES_DIRS[0]},
)
urlpatterns = [
    # path("tz_detect/", include("tz_detect.urls")),
    # path("pricing", pricing, name="pricing"),
    path("dashboard/settings/", include("core.views.settings.urls")),
    path("dashboard/teams/", include("core.views.teams.urls")),
    path("dashboard/emails/", include("core.views.emails.urls")),
    path("favicon.ico", RedirectView.as_view(url=settings.STATIC_URL + "favicon.ico")),
    path("login/external/", include("social_django.urls", namespace="social")),
    path("auth/", include("core.views.auth.urls")),
    path("api/", include("core.api.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

app_name = "core"

if settings.DEBUG:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # may not need to be in debug
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

schema_view = get_swagger_ui()
urlpatterns += get_swagger_endpoints(settings.DEBUG)

handler500 = "core.views.other.errors.universal"
handler404 = "core.views.other.errors.universal"
handler403 = "core.views.other.errors.e_403"
