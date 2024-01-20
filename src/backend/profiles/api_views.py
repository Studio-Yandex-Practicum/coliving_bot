from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Location, Profile, UserFromTelegram
from .serializers import ProfileSerializer


class ProfileView(
    generics.CreateAPIView, generics.RetrieveAPIView, generics.UpdateAPIView
):
    """
    Вью-класс для отображения, сохранения и обновления объектов 'Profile'.
    """

    serializer_class = ProfileSerializer
    http_method_names = ["get", "post", "patch"]

    def get_object(self) -> Profile:
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            user=get_object_or_404(
                UserFromTelegram, telegram_id=self.kwargs.get("telegram_id")
            ),
        )
        return obj

    def get_queryset(self) -> Profile:
        profile = Profile.objects.filter(
            user=get_object_or_404(
                UserFromTelegram, telegram_id=self.kwargs.get("telegram_id")
            )
        )
        if profile.exists():
            return profile
        raise NotFound(detail="Профиль не найден", code=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer) -> None:
        user, _is_created = UserFromTelegram.objects.get_or_create(
            telegram_id=self.kwargs.get("telegram_id")
        )
        location_id, _is_created = Location.objects.get_or_create(
            name=self.request.data.get("location")
        )
        serializer.save(
            user=user,
            location=location_id,
            is_visible=False,
        )

    def perform_update(self, serializer) -> None:
        try:
            location = Location.objects.get(name=self.request.data.get("location"))
        except ObjectDoesNotExist:
            location = self.get_object().location
        serializer.save(
            user=get_object_or_404(
                UserFromTelegram, telegram_id=self.kwargs.get("telegram_id")
            ),
            location=location,
            is_visible=self.request.data.get("is_visible", False),
        )

    def patch(self, request, *args, **kwargs) -> Response:
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
