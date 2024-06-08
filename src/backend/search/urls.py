from django.conf import settings
from django.urls import path

from search.views import (
    ColivingLikeCreateAPIView,
    ColivingLikesListAPIView,
    ColivingLikeUpdateAPIView,
    MatchedProfileListAPIView,
    PotentialRoommatesListAPIView,
    ProfileLikeCreateAPIView,
    ProfileLikeDestroyAPIView,
    ProfileLikeUpdateAPIView,
    ProfilesSearchView,
    UserReportCreateView,
)

app_name = "search"

urlpatterns = [
    path(
        f"{settings.API_V1_PREFIX}/users/<int:telegram_id>/matches/",
        MatchedProfileListAPIView.as_view(),
        name="matched_profile_likes",
    ),
    path(
        f"{settings.API_V1_PREFIX}/colivings/<int:pk>/matches/",
        ColivingLikesListAPIView.as_view(),
        name="matched_coliving_likes",
    ),
    path(
        f"{settings.API_V1_PREFIX}/colivings/<int:pk>/potential-roommates/",
        PotentialRoommatesListAPIView.as_view(),
        name="potential-roommates",
    ),
    path(
        f"{settings.API_V1_PREFIX}/reports/",
        UserReportCreateView.as_view(),
        name="report",
    ),
    path(
        f"{settings.API_V1_PREFIX}/profiles/",
        ProfilesSearchView.as_view(),
        name="profiles",
    ),
    path(
        f"{settings.API_V1_PREFIX}/profiles/like/",
        ProfileLikeCreateAPIView.as_view(),
        name="profile-like-create",
    ),
    path(
        f"{settings.API_V1_PREFIX}/profiles/like/<int:pk>/",
        ProfileLikeUpdateAPIView.as_view(),
        name="profile-like-update",
    ),
    path(
        f"{settings.API_V1_PREFIX}/profiles/like/delete_old_likes/",
        ProfileLikeDestroyAPIView.as_view(),
        name="profile-like-delete",
    ),
    path(
        f"{settings.API_V1_PREFIX}/colivings/like/",
        ColivingLikeCreateAPIView.as_view(),
        name="coliving-like-create",
    ),
    path(
        f"{settings.API_V1_PREFIX}/colivings/like/<int:pk>/",
        ColivingLikeUpdateAPIView.as_view(),
        name="coliving-like-update",
    ),
]
