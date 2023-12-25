from django.urls import path

from .api_views import ColivingImageView, ProfileImageView

urlpatterns = [
    path("v1/profiles/<int:id>/images/", ProfileImageView.as_view()),
    path("v1/colivings/<int:id>/images/", ColivingImageView.as_view()),
]
