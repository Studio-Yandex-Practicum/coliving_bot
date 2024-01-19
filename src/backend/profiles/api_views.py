from typing import Type

from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Location, Profile, UserFromTelegram
from .serializers import (
    ProfileCreateSerializer,
    ProfileReadSerializer,
    ProfileUpdateSerializer,
)


class BaseProfileView(generics.ListCreateAPIView):
    """
    Базовый вью-класс объектов 'Profile'.
    """

    def _get_telegram_user(self) -> UserFromTelegram:
        """
        Возвращает объект 'UserFromTelegram'.
        """
        return get_object_or_404(
            UserFromTelegram, telegram_id=self.kwargs.get("telegram_id")
        )

    def _get_location_name(self) -> Location:
        """
        Возвращает объект 'Location'.
        """
        location_name = self.request.data.get("location")
        return Location.objects.filter(name=location_name).first()


class ProfileView(BaseProfileView):
    """
    Вью-класс для отображения, сохранения и обновления объектов 'Profile'.
    """

    queryset = Profile.objects.all()
    http_method_names = ["get", "post", "patch"]
    lookup_field = "user"

    def get_serializer_class(
        self,
    ) -> Type[
        (ProfileCreateSerializer | ProfileReadSerializer | ProfileUpdateSerializer)
    ]:
        if self.request.method == "GET":
            return ProfileReadSerializer
        elif self.request.method == "POST":
            return ProfileCreateSerializer
        elif self.request.method == "PATCH":
            return ProfileUpdateSerializer

    def get_object(self) -> Profile:
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self._get_telegram_user())
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self) -> Profile:
        profile = Profile.objects.filter(user=self._get_telegram_user())
        if profile.exists():
            return profile
        raise NotFound(detail="Профиль не найден", code=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer) -> None:
        serializer.save(
            user=self._get_telegram_user(),
            location=self._get_location_name(),
            is_visible=False,
        )

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(
            data=request.data, context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_update(self, serializer) -> None:
        location_id = self._get_location_name()

        if location_id is not None:
            serializer.save(
                user=self._get_telegram_user(),
                location=location_id,
                is_visible=self.request.data.get("is_visible", False),
            )
        else:
            serializer.save(
                user=self._get_telegram_user(),
                is_visible=self.request.data.get("is_visible", False),
            )

    def patch(self, request, *args, **kwargs) -> Response:
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
