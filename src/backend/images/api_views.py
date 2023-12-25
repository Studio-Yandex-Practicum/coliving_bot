from typing import Union

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS

from profiles.models import Coliving, Profile

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

    async def _get_object(
        self, model: Union[Coliving, Profile]
    ) -> list[Union[Coliving, Profile]]:
        """Возвращает объекты 'Profile' или 'Coliving'."""
        return get_object_or_404(model, id=self.kwargs.get("id"))


class ProfileImageView(BaseImage):
    """
    Вью-класс для отображения и сохранения объектов 'ProfileImage'.
    """

    def get_queryset(self):
        return ProfileImage.objects.filter(
            profile=self._get_object(Profile).id
        )

    def get_serializer_class(self):
        return (
            ProfileImageReadSerializer
            if self.request.method in SAFE_METHODS
            else ProfileImageCreateSerializer
        )

    def perform_create(self, serializer):
        serializer.save(profile=self._get_object(Profile))


class ColivingImageView(BaseImage):
    """
    Вью-класс для отображения и сохранения объектов 'ColivingImage'.
    """

    def get_queryset(self):
        return ColivingImage.objects.filter(
            coliving=self._get_object(Coliving).id
        )

    def get_serializer_class(self):
        return (
            ColivingImageReadSerializer
            if self.request.method in SAFE_METHODS
            else ColivingImageCreateSerializer
        )

    def perform_create(self, serializer):
        serializer.save(coliving=self._get_object(Coliving))
