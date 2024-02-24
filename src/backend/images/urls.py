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
        f"{settings.API_V1_PREFIX}/users/<int:telegram_id>/profile/images/<int:pk>/",
        ProfileImageView.as_view(),
        name='profile-image-detail'
    ),
    path(
        (
            f"{settings.API_V1_PREFIX}/users/<int:telegram_id>/"
            "colivings/<int:coliving_id>/images/"
        ),
        ColivingImageView.as_view(),
    ),
    path(
        "users/<int:telegram_id>/colivings/<int:coliving_id>/images/<int:pk>/",
        ColivingImageView.as_view(),
        name='coliving-image-detail'
    ),
]
