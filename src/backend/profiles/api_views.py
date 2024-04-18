from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

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
    generics.RetrieveAPIView,
    generics.UpdateAPIView,
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

    def get_queryset(self):
        queryset = super().get_queryset()

        viewer = self.request.query_params.get("viewer", None)
        if viewer:
            try:
                user = UserFromTelegram.objects.get(telegram_id=viewer)
            except ObjectDoesNotExist:
                user = None

            excl_list = Coliving.objects.filter(
                Q(host=user) | Q(viewers=user)
            ).values_list("pk", flat=True)
            queryset = queryset.filter(is_visible=True).exclude(pk__in=excl_list)

        return queryset


class ColivingDetailView(
    DestroyWithMediaRemovalMixin, generics.RetrieveUpdateDestroyAPIView
):
    """Apiview для обновления Coliving."""

    queryset = Coliving.objects.select_related("location", "host").all()
    serializer_class = ColivingSerializer


class ColivingRoommatesView(generics.ListAPIView):
    serializer_class = RoommatesSerializer
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        return UserFromTelegram.objects.filter(residence_id=self.kwargs["pk"])


class UserResidenceUpdateAPIView(generics.UpdateAPIView):
    """Apiview представление для обновления информации о проживании пользователя.
    Обрабатывает PATCH-запросы на адрес /api/v1/users/{telegram_id}/,
    позволяя прикреплять пользователя к определенному коливингу
    или откреплять его
    """

    queryset = UserFromTelegram.objects.all()
    serializer_class = UserResidenceSerializer
    lookup_field = "telegram_id"
