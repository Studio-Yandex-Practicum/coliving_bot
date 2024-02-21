from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.generics import get_object_or_404

from profiles.filters import ColivingFilter
from profiles.models import Coliving, Location, Profile, UserFromTelegram
from profiles.serializers import (
    ColivingSerializer,
    LocationSerializer,
    ProfileSerializer,
    UserResidenceSerializer,
)


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


class LocationList(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ColivingView(generics.ListCreateAPIView):
    """Apiview для создания и получения Coliving."""

    queryset = (
        Coliving.objects.select_related("location", "host")
        .prefetch_related("images")
        .all()
    )
    serializer_class = ColivingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ColivingFilter


class ColivingDetailView(generics.RetrieveUpdateAPIView):
    """Apiview для обновления Coliving."""

    queryset = Coliving.objects.select_related("location", "host").all()
    serializer_class = ColivingSerializer


class UserResidenceUpdateAPIView(generics.UpdateAPIView):
    """Apiview представление для обновления информации о проживании пользователя.
    Обрабатывает PATCH-запросы на адрес /api/v1/users/{telegram_id}/,
    позволяя прикреплять пользователя к определенному коливингу
    или откреплять его
    """

    queryset = UserFromTelegram.objects.all()
    serializer_class = UserResidenceSerializer
    lookup_field = "telegram_id"
