from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/", include("search.urls")),
    path("admin/", admin.site.urls),
]
