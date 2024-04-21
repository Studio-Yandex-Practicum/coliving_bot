from django.conf import settings
from django.urls import path

from search.views import (
    MatchedUsersListView,
    MatchRequestListCreateView,
    MatchRequestUpdateView,
    ProfilesSearchView,
    UserReportCreateView,
)

app_name = "search"


urlpatterns = [
    path(
        f"{settings.API_V1_PREFIX}/users/<int:telegram_id>/matches/",
        MatchedUsersListView.as_view(),
        name="matched-users",
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
        f"{settings.API_V1_PREFIX}/match_requests/",
        MatchRequestListCreateView.as_view(),
        name="match-request",
    ),
    path(
        f"{settings.API_V1_PREFIX}/match_requests/<int:pk>/",
        MatchRequestUpdateView.as_view(),
        name="patch-match-request",
    ),
]
