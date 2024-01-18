from typing import Type

from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from .models import Profile, UserFromTelegram, Location
from .serializers import ProfileCreateSerializer, ProfileReadSerializer


class ProfileView(generics.ListCreateAPIView):

    queryset = Profile.objects.all()
    http_method_names = ["get", "post"]
    lookup_field = "user"

    def get_serializer_class(
        self
    ) -> Type[ProfileCreateSerializer | ProfileReadSerializer]:
        return (
            ProfileReadSerializer
            if self.request.method in SAFE_METHODS
            else ProfileCreateSerializer
        )

    def perform_create(self, serializer) -> None:
        telegram_id = self.kwargs.get("telegram_id")
        user = UserFromTelegram.objects.get(telegram_id=telegram_id)
        location_name = self.request.data.get("location")
        location_id = Location.objects.filter(
            name=location_name).first()
        serializer.save(user=user, location=location_id, is_visible=False)

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(
            data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)
