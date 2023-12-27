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


class ProfileImageView(generics.ListCreateAPIView):
    """
    Вью-класс для отображения и сохранения объектов 'ProfileImage'.
    """

    def get_queryset(self):
        telegram_user = get_object_or_404(
            UserFromTelegram, telegram_id=self.kwargs.get("telegram_id")
        )
        profile = Profile.objects.filter(user=telegram_user)
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

    # def perform_create(self, serializer):
    #     serializer.save(profile=get_object_or_404(Profile))


class ColivingImageView(generics.ListCreateAPIView):
    """
    Вью-класс для отображения и сохранения объектов 'ColivingImage'.
    """

    def get_queryset(self):
        telegram_user = get_object_or_404(
            UserFromTelegram, telegram_id=self.kwargs.get("telegram_id")
        )
        colivings = telegram_user.colivings.filter(
            id=self.kwargs.get("coliving_id")
        )
        if colivings.exists():
            return colivings.first().images.all()
        raise NotFound(
            detail="Коливинг не найден", code=status.HTTP_404_NOT_FOUND
        )

    def get_serializer_class(self):
        return (
            ColivingImageReadSerializer
            if self.request.method in SAFE_METHODS
            else ColivingImageCreateSerializer
        )

    # def perform_create(self, serializer):
    #     serializer.save(coliving=self.get_object_or_404(Coliving))
