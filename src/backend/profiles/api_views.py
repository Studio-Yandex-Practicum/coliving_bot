from rest_framework import generics

from .models import UserFromTelegram
from .serializers import UserSerializer


class UpdateUserLocationView(generics.UpdateAPIView):
    """Вью-класс для обновления места проживания пользователя."""

    serializer_class = UserSerializer
    queryset = UserFromTelegram.objects.all()
    lookup_field = "telegram_id"
