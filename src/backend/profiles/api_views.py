from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404

from .models import Profile, UserFromTelegram
from .serializers import ProfileSerializer


class ProfileView(
    generics.CreateAPIView, generics.RetrieveAPIView, generics.UpdateAPIView
):
    """
    Вью-класс для отображения, сохранения и обновления объектов 'Profile'.
    """

    # queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # lookup_field = "user"
    # lookup_url_kwarg = "telegram_id"
    http_method_names = ["get", "post", "patch"]

    def get_object(self) -> Profile:
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            user=get_object_or_404(
                UserFromTelegram, telegram_id=self.kwargs.get("telegram_id")
            ),
        )
        return obj

    def get_queryset(self) -> Profile:
        profile = Profile.objects.filter(
            user=get_object_or_404(
                UserFromTelegram, telegram_id=self.kwargs.get("telegram_id")
            )
        )
        if profile.exists():
            return profile
        raise NotFound(detail="Профиль не найден", code=status.HTTP_404_NOT_FOUND)

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
