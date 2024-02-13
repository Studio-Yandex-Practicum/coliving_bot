from django.contrib import admin
from django.urls import include, path

api_urlpatterns = [
    path("/", include("profiles.urls")),
    path("/", include("search.urls")),
    path("/", include("images.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include((api_urlpatterns, "api-v1"), namespace="api-v1")),
]
