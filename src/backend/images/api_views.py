import os
import shutil
from typing import Tuple, Type

from django.conf import settings
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from profiles.models import Coliving, Profile

from .models import ColivingImage, ProfileImage
from .serializers import (
    ColivingImageCreateSerializer,
    ColivingImageReadSerializer,
    ProfileImageCreateSerializer,
    ProfileImageReadSerializer,
)


class BaseImageView(generics.ListCreateAPIView, generics.UpdateAPIView):
    """
    Базовый вью-класс объектов 'ProfileImage', 'ColivingImage'.
    Позволяет получать список изображений, создавать новые,
    получать детали по конкретному изображению и удалять их.
    """

    def _get_image_directory(self) -> Tuple[str, str]:
        """
        Возвращает имя директории и идентификатор объекта для удаления.
        """
        raise NotImplementedError()

    def delete(self, request, *args, **kwargs) -> Response:
        images = self.get_queryset()

        obj_dir, obj_id = self._get_image_directory()

        images.delete()

        path = os.path.join(settings.MEDIA_ROOT, obj_dir, obj_id)
        shutil.rmtree(path)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileImageView(BaseImageView):
    """
    Вью-класс для отображения и сохранения объектов 'ProfileImage'.
    """

    def get_queryset(self) -> QuerySet[ProfileImage]:
        return ProfileImage.objects.filter(
            profile__user__telegram_id=self.kwargs.get("telegram_id")
        ).all()

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

    def _get_image_directory(self) -> Tuple[str, str]:
        profile_pk = (
            Profile.objects.values_list("id", flat=True)
            .filter(user__telegram_id=self.kwargs.get("telegram_id"))
            .first()
        )
        if profile_pk is None:
            raise NotFound("Профиль не найден.")
        else:
            return "profiles", str(profile_pk)


class ColivingImageView(BaseImageView):
    """
    Вью-класс для отображения и сохранения объектов 'ColivingImage'.
    """

    def get_queryset(self) -> QuerySet[ColivingImage]:
        return ColivingImage.objects.filter(
            coliving__host__telegram_id=self.kwargs.get("telegram_id"),
            coliving__id=self.kwargs.get("coliving_id"),
        ).all()

    def get_serializer_class(
        self,
    ) -> Type[ColivingImageReadSerializer | ColivingImageCreateSerializer]:
        return (
            ColivingImageReadSerializer
            if self.request.method in SAFE_METHODS
            else ColivingImageCreateSerializer
        )

    def perform_create(self, serializer: ColivingImageCreateSerializer) -> None:
        serializer.save(
            coliving=get_object_or_404(Coliving, id=self.kwargs.get("coliving_id"))
        )

    def _get_image_directory(self) -> Tuple[str, str]:
        coliving_pk = (
            Coliving.objects.values_list("id", flat=True)
            .filter(id=self.kwargs.get("coliving_id"))
            .first()
        )
        if coliving_pk is None:
            raise NotFound("Коливинг не найден.")
        else:
            return "colivings", str(coliving_pk)
