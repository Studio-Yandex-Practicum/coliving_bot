from django.conf import settings
from django.urls import path

from images.api_views import ColivingImageView, ProfileImageView

app_name = "images"

urlpatterns = [
    path(
        f"{settings.API_V1_PREFIX}/users/<int:telegram_id>/profile/images/",
        ProfileImageView.as_view(),
    ),
    path(
        (
            f"{settings.API_V1_PREFIX}/users/<int:telegram_id>/"
            "colivings/<int:coliving_id>/images/"
        ),
        ColivingImageView.as_view(),
    ),
]
