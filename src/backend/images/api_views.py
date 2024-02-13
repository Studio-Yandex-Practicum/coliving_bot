from typing import Type

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import SAFE_METHODS

from profiles.models import Coliving, Profile, UserFromTelegram

from .models import ColivingImage, ProfileImage
from .serializers import (
    ColivingImageCreateSerializer,
    ColivingImageReadSerializer,
    ProfileImageCreateSerializer,
    ProfileImageReadSerializer,
)


class BaseImageView(generics.ListCreateAPIView):
    """
    Базовый вью-класс объектов 'ProfileImage', 'ColivingImage'.
    """

    def _get_telegram_user(self) -> UserFromTelegram:
        """
        Возвращает объект 'UserFromTelegram'.
        """
        return get_object_or_404(
            UserFromTelegram, telegram_id=self.kwargs.get("telegram_id")
        )

    def _get_coliving(self) -> Coliving:
        """
        Возвращает объект 'Coliving'.
        """

        telegram_user_colivings: QuerySet[
            Coliving
        ] = self._get_telegram_user().colivings.filter(
            id=self.kwargs.get("coliving_id")
        )
        if not telegram_user_colivings.exists():
            raise NotFound(detail="Коливинг не найден", code=status.HTTP_404_NOT_FOUND)
        return telegram_user_colivings.first()


class ProfileImageView(BaseImageView):
    """
    Вью-класс для отображения и сохранения объектов 'ProfileImage'.
    """

    def get_queryset(self) -> list[ProfileImage]:
        profile: QuerySet[Profile] = Profile.objects.filter(
            user=self._get_telegram_user()
        )
        if profile.exists():
            return profile.first().images.all()
        raise NotFound(detail="Профиль не найден", code=status.HTTP_404_NOT_FOUND)

    def get_serializer_class(
        self,
    ) -> Type[ProfileImageReadSerializer | ProfileImageCreateSerializer]:
        return (
            ProfileImageReadSerializer
            if self.request.method in SAFE_METHODS
            else ProfileImageCreateSerializer
        )

    def perform_create(self, serializer: ProfileImageCreateSerializer) -> None:
        serializer.save(
            profile=get_object_or_404(
                Profile, user__telegram_id=self.kwargs.get("telegram_id")
            )
        )


class ColivingImageView(BaseImageView):
    """
    Вью-класс для отображения и сохранения объектов 'ColivingImage'.
    """

    def get_queryset(self) -> list[ColivingImage]:
        return self._get_coliving().images.all()

    def get_serializer_class(
        self,
    ) -> Type[ColivingImageReadSerializer | ColivingImageCreateSerializer]:
        return (
            ColivingImageReadSerializer
            if self.request.method in SAFE_METHODS
            else ColivingImageCreateSerializer
        )

    def perform_create(self, serializer: ColivingImageCreateSerializer) -> None:
        serializer.save(coliving=self._get_coliving())
