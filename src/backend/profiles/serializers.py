from rest_framework import serializers

from .models import Coliving, Location, UserFromTelegram


class ColivingSerializer(serializers.ModelSerializer):
    """Сериализатор для Coliving."""
    host = serializers.SlugRelatedField(
        slug_field="telegram_id", queryset=UserFromTelegram.objects.all())

    location = serializers.SlugRelatedField(
        slug_field="name", queryset=Location.objects.all())

    class Meta:

        model = Coliving
        fields = ("id", "host", "location", "price", "room_type", "about")
