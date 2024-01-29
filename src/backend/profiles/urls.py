from django.urls import path

from .api_views import UpdateUserLocationView

API_V1_PREFIX = "v1"


urlpatterns = [
    path(
        f"{API_V1_PREFIX}/users/<int:telegram_id>/",
        UpdateUserLocationView.as_view(),
        name="update-user-location",
    )
]
