from rest_framework import generics

from profiles.models import Location, Profile, UserFromTelegram
from profiles.serializers import LocationSerializer, ProfileSerializer


class ProfileView(
    generics.CreateAPIView, generics.RetrieveAPIView, generics.UpdateAPIView
):
    """
    Вью-класс для отображения, сохранения и обновления объектов 'Profile'.
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "user__telegram_id"
    lookup_url_kwarg = "telegram_id"
    http_method_names = ["get", "post", "patch"]

    def perform_create(self, serializer) -> None:
        user, _is_created = UserFromTelegram.objects.get_or_create(
            telegram_id=self.kwargs.get("telegram_id")
        )
        serializer.save(
            user=user,
        )


class LocationList(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
