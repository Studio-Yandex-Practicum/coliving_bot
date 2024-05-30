from django.conf import settings
from django.urls import path

from profiles.api_views import (
    ColivingDetailView,
    ColivingRoommatesView,
    ColivingView,
    LocationList,
    ProfileView,
    UserResidenceAPIView,
)

app_name = "profiles"

urlpatterns = [
    path(
        f"{settings.API_V1_PREFIX}/users/<int:telegram_id>/profile/",
        ProfileView.as_view(),
        name="user-profile",
    ),
    path(
        f"{settings.API_V1_PREFIX}/locations/",
        LocationList.as_view(),
        name="locations-list",
    ),
    path(
        "v1/colivings/<int:pk>/roommates/",
        ColivingRoommatesView.as_view(),
        name="colivings-roommates",
    ),
    path("v1/colivings/", ColivingView.as_view(), name="colivings-list"),
    path(
        "v1/colivings/<int:pk>/", ColivingDetailView.as_view(), name="colivings-detail"
    ),
    path(
        f"{settings.API_V1_PREFIX}/users/<int:telegram_id>/",
        UserResidenceAPIView.as_view(),
        name="users-detail",
    ),
]
