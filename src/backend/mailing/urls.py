from django.conf import settings
from django.urls import path

from .api_views import MailingView, UserMailView

app_name = "mailings"

urlpatterns = [
    path(
        f"{settings.API_V1_PREFIX}/mailings/",
        MailingView.as_view({"get": "list"}),
    ),
    path(
        f"{settings.API_V1_PREFIX}/mailings/users/",
        UserMailView.as_view({"get": "list"}),
    ),
    path(
        f"{settings.API_V1_PREFIX}/mailings/<int:pk>/",
        MailingView.as_view({"patch": "partial_update"}),
    ),
]
