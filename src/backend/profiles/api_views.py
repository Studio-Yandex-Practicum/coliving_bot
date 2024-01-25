from rest_framework import generics
from rest_framework.generics import get_object_or_404

from .models import Profile, UserFromTelegram
from .serializers import ProfileSerializer


class ProfileView(
    generics.CreateAPIView, generics.RetrieveAPIView, generics.UpdateAPIView
):
    """
    Вью-класс для отображения, сохранения и обновления объектов 'Profile'.
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "user__telegram_id"
    lookup_url_kwarg = "telegram_id"
    http_method_names = ["get", "post", "patch"]

    def perform_create(self, serializer) -> None:
        user, _is_created = UserFromTelegram.objects.get_or_create(
            telegram_id=self.kwargs.get("telegram_id")
        )
        serializer.save(
            user=user,
            is_visible=False,
        )

    def perform_update(self, serializer) -> None:
        serializer.save(
            user=get_object_or_404(
                UserFromTelegram, telegram_id=self.kwargs.get("telegram_id")
            ),
            is_visible=self.request.data.get("is_visible", False),
        )
