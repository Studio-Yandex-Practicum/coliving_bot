from rest_framework import serializers

from profiles.models import Coliving, Location, Profile, UserFromTelegram


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "name"]


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор объекта 'Profile' (безопасные методы).
    """

    user = serializers.SerializerMethodField()
    location = serializers.SlugRelatedField(
        queryset=Location.objects.all(), slug_field="name"
    )

    class Meta:
        model = Profile
        fields = (
            "user",
            "name",
            "sex",
            "age",
            "location",
            "about",
            "is_visible",
        )

    @staticmethod
    def get_user(obj):
        return obj.user.telegram_id


class ColivingSerializer(serializers.ModelSerializer):
    """Сериализатор для Coliving."""

    host = serializers.SlugRelatedField(
        slug_field="telegram_id", queryset=UserFromTelegram.objects.all()
    )
    location = serializers.SlugRelatedField(
        slug_field="name", queryset=Location.objects.all()
    )
    images = serializers.SlugRelatedField(
        slug_field="file_id", many=True, read_only=True
    )

    class Meta:
        model = Coliving
        fields = (
            "id",
            "host",
            "location",
            "price",
            "room_type",
            "about",
            "images",
        )
