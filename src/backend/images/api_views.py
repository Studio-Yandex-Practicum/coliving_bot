from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS
from rest_framework.exceptions import NotFound

from profiles.models import Coliving, UserFromTelegram

from .models import ColivingImage, ProfileImage
from .serializers import (
    ColivingImageCreateSerializer,
    ColivingImageReadSerializer,
    ProfileImageCreateSerializer,
    ProfileImageReadSerializer,
)


class BaseImage(generics.ListCreateAPIView):
    """
    Базовый вью-класс объектов 'ProfileImage', 'ColivingImage'.
    """

    def _get_object(self, model, **kwargs):
        """Возвращает объекты 'Profile' или 'Coliving'."""
        return get_object_or_404(model, **kwargs)


class ProfileImageView(BaseImage):
    """
    Вью-класс для отображения и сохранения объектов 'ProfileImage'.
    """

    def get_queryset(self):
        return ProfileImage.objects.filter(
            profile__user__telegram_id=self._get_object(
                UserFromTelegram, telegram_id=self.kwargs.get("telegram_id")
            ).telegram_id
        )

    def get_serializer_class(self):
        return (
            ProfileImageReadSerializer
            if self.request.method in SAFE_METHODS
            else ProfileImageCreateSerializer
        )

    def perform_create(self, serializer: ProfileImageCreateSerializer):
        serializer.save(profile=self._get_object(Profile))


class ColivingImageView(generics.ListCreateAPIView):
    """
    Вью-класс для отображения и сохранения объектов 'ColivingImage'.
    """

    def get_queryset(self):
        telegram_user = get_object_or_404(
            UserFromTelegram, telegram_id=self.kwargs.get("telegram_id")
        )
        colivings = telegram_user.colivings.filter(id=self.kwargs.get("coliving_id"))
        if colivings.exists():
            return colivings.first().images.all()
        raise NotFound(detail="Коливинг не найден", code=status.HTTP_404_NOT_FOUND)

    def get_serializer_class(self):
        return (
            ColivingImageReadSerializer
            if self.request.method in SAFE_METHODS
            else ColivingImageCreateSerializer
        )

    def perform_create(self, serializer: ColivingImageCreateSerializer):
        serializer.save(coliving=self._get_object(Coliving))
