from django.urls import path

from search.views import MatchedUsersListView, UserReportCreateView, MatchRequestView

API_V1_PREFIX = "v1"
app_name = "api-v1"

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

    path(
        f"{API_V1_PREFIX}/match_requests/",
        MatchRequestView.as_view(),
        name="match-request",
    ),]