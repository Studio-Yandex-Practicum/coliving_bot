from django.urls import path

from .api_views import ColivingImageView, ProfileImageView

urlpatterns = [
    path("v1/users/<int:telegram_id>/profile/images/", ProfileImageView.as_view()),
    path(
        "v1/users/<int:telegram_id>/coliving/<int:coliving_id>/images/",
        ColivingImageView.as_view(),
    ),
]
