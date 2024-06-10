from django.conf import settings
from django.urls import path

from .api_views import MailingView, UserMailView

app_name = "mailing"

urlpatterns = [
    path(
        f"{settings.API_V1_PREFIX}/mailing/",
        MailingView.as_view({"get": "list"}),
    ),
    path(
        f"{settings.API_V1_PREFIX}/mailing/users/",
        UserMailView.as_view({"get": "list"}),
    ),
    path(
        f"{settings.API_V1_PREFIX}/mailing/<int:pk>/",
        MailingView.as_view({"patch": "partial_update"}),
    ),
]
