from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS

from profiles.models import Coliving, Profile

from .models import ColivingImage, ProfileImage
from .serializers import (
    ColivingImageReadSerializer,
    ProfileImageCreateSerializer,
    ProfileImageReadSerializer,
)


class ProfileImageList(generics.ListCreateAPIView, generics.DestroyAPIView):
    """
    Вью-класс для отображения и сохранения объектов 'ProfileImage'.
    """

    def __get_profile_object(self):
        """Возвращает объект 'Profile'."""
        return get_object_or_404(Profile, id=self.kwargs.get("id"))

    def get_queryset(self):
        return ProfileImage.objects.filter(
            profile=self.__get_profile_object().id
        )

    def get_serializer_class(self):
        return (
            ProfileImageReadSerializer
            if (self.request.method in SAFE_METHODS)
            else ProfileImageCreateSerializer
        )

    def perform_create(self, serializer):
        serializer.save(profile=self.__get_profile_object())


class ColivingImageList(generics.ListCreateAPIView):
    """
    Вью-класс для отображения и сохранения объектов 'ColivingImage'.
    """

    serializer_class = ColivingImageReadSerializer

    def get_queryset(self):
        coliving_obj = get_object_or_404(Coliving, id=self.kwargs.get("id"))

        return ColivingImage.objects.filter(coliving=coliving_obj.id)
