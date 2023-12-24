from django.urls import path

from .api_views import ColivingImageList, ProfileImageList

urlpatterns = [
    path("v1/profiles/<int:id>/images/", ProfileImageList.as_view()),
    path("v1/colivings/<int:id>/images/", ColivingImageList.as_view()),
]
