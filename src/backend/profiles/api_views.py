from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from profiles.filters import ColivingFilter, SmallResultsSetPagination
from profiles.mixins import DestroyWithMediaRemovalMixin
from profiles.models import Coliving, Location, Profile, UserFromTelegram
from profiles.serializers import (
    ColivingSerializer,
    LocationSerializer,
    ProfileSerializer,
    RoommatesSerializer,
    UserResidenceSerializer,
)


class ProfileView(
    generics.CreateAPIView,
    DestroyWithMediaRemovalMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    """
    Вью-класс для отображения, сохранения и обновления объектов 'Profile'.
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "user__telegram_id"
    lookup_url_kwarg = "telegram_id"
    http_method_names = ["get", "post", "patch", "delete"]

    def perform_create(self, serializer) -> None:
        user, _is_created = UserFromTelegram.objects.get_or_create(
            telegram_id=self.kwargs.get("telegram_id")
        )
        serializer.save(
            user=user,
        )


class LocationList(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ColivingView(generics.ListCreateAPIView):
    """Apiview для создания и получения Coliving."""

    queryset = Coliving.objects.select_related("location", "host").prefetch_related(
        "images"
    )
    serializer_class = ColivingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ColivingFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        viewer = self.request.query_params.get("viewer")
        if viewer is None:
            return queryset.all()
        user_profile = get_object_or_404(Profile, user_id=viewer)
        return (
            queryset.exclude(
                id__in=user_profile.liked_colivings.values_list(
                    "coliving__id",
                    flat=True,
                ),
            )
            .exclude(
                id__in=user_profile.user.colivings.values_list(
                    "id",
                    flat=True,
                ),
            )
            .filter(is_visible=True)
            .all()
        )


class ColivingDetailView(
    DestroyWithMediaRemovalMixin, generics.RetrieveUpdateDestroyAPIView
):
    """Apiview для обновления Coliving."""

    queryset = Coliving.objects.select_related("location", "host").all()
    serializer_class = ColivingSerializer


class ColivingRoommatesView(generics.ListAPIView):
    """Apiview для получения списка соседей."""

    serializer_class = RoommatesSerializer
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        """Возвращает пользователей, отфильтрованных по идентификатору коливинга."""
        return (
            UserFromTelegram.objects.select_related("user_profile")
            .values("user_profile__age", "user_profile__name", "telegram_id")
            .filter(residence_id=self.kwargs["pk"])
        )


class UserResidenceAPIView(generics.UpdateAPIView, generics.RetrieveAPIView):
    """
    Apiview представление для обновления информации о проживании пользователя.
    Обрабатывает Update/Get на адрес /api/v1/users/{telegram_id}/,
    позволяя получать текущий, прикреплять пользователя к определенному коливингу
    или откреплять его.
    """

    queryset = UserFromTelegram.objects.all()
    serializer_class = UserResidenceSerializer
    lookup_field = "telegram_id"

    def get(self, request, *args, **kwargs):
        """Получить коливинг текущего проживающего."""

        telegram_id = self.kwargs.get("telegram_id")
        user = UserFromTelegram.objects.get(telegram_id=telegram_id)
        coliving_profile = user.residence
        if coliving_profile:
            coliving_data = ColivingSerializer(coliving_profile).data
            return Response(coliving_data)
        return Response(status=status.HTTP_204_NO_CONTENT)
