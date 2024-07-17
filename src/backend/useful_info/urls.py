from django.conf import settings
from django.urls import path

from useful_info.views import UsefulMaterialListAPIView

app_name = "useful_info"

urlpatterns = [
    path(
        f"{settings.API_V1_PREFIX}/useful-materials/",
        UsefulMaterialListAPIView.as_view(),
        name="useful-materials-list",
    ),
]
