from django.urls import path

from .api_views import ProfileView

urlpatterns = [
    path(
        "v1/users/<int:telegram_id>/profile/",
        ProfileView.as_view(),
        name="profiles",
    ),
]
