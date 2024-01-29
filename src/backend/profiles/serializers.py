from rest_framework import serializers

from .models import UserFromTelegram


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = UserFromTelegram
        fields = ("residence",)
        extra_kwargs = {"residence": {"required": True}}
