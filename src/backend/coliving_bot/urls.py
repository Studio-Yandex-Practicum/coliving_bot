from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/", include("search.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("images.urls")),
    path("api/", include("profiles.urls", namespace="api-v1")),
]
