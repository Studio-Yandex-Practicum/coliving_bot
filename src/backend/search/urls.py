from django.conf import settings
from django.urls import path

from search.views import MatchedUsersListView, UserReportCreateView

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
]
