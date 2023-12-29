from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import SAFE_METHODS

from profiles.models import Profile, UserFromTelegram

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

    def _get_telegram_user(self):
        """Возвращает объект 'UserFromTelegram'."""
        return get_object_or_404(
            UserFromTelegram, telegram_id=self.kwargs.get("telegram_id")
        )

    def _get_colivings(self):
        """Возвращает объект 'Coliving'."""

        telegram_user_colivings = self._get_telegram_user().colivings.filter(
            id=self.kwargs.get("coliving_id")
        )
        if not telegram_user_colivings.exists():
            raise NotFound(
                detail="Коливинг не найден", code=status.HTTP_404_NOT_FOUND
            )
        return telegram_user_colivings.first()


class ProfileImageView(BaseImageView):
    """
    Вью-класс для отображения и сохранения объектов 'ProfileImage'.
    """

    def get_queryset(self):
        profile = Profile.objects.filter(user=self._get_telegram_user())
        if profile.exists():
            return profile.first().images.all()
        raise NotFound(
            detail="Профиль не найден", code=status.HTTP_404_NOT_FOUND
        )

    def get_serializer_class(self):
        return (
            ProfileImageReadSerializer
            if self.request.method in SAFE_METHODS
            else ProfileImageCreateSerializer
        )

    def perform_create(self, serializer):
        serializer.save(
            profile=get_object_or_404(
                Profile, user__telegram_id=self.kwargs.get("telegram_id")
            )
        )


class ColivingImageView(BaseImageView):
    """
    Вью-класс для отображения и сохранения объектов 'ColivingImage'.
    """

    def get_queryset(self):
        return self._get_colivings().images.all()

    def get_serializer_class(self):
        return (
            ColivingImageReadSerializer
            if self.request.method in SAFE_METHODS
            else ColivingImageCreateSerializer
        )

    def perform_create(self, serializer):
        serializer.save(coliving=self._get_colivings())
