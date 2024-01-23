from django.urls import path

from search.views import MatchedUsersListView, UserReportCreateView

API_V1_PREFIX = "v1"

urlpatterns = [
    path(
        f"{API_V1_PREFIX}/users/<int:telegram_id>/matches/",
        MatchedUsersListView.as_view(),
        name="matched-users",
    ),
    path(
        f"{API_V1_PREFIX}/reports/",
        UserReportCreateView.as_view(),
        name="report",
    ),
]
