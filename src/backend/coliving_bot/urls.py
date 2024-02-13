from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("api/", include("search.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("images.urls")),
    path("api/", include("profiles.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # документация API:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
