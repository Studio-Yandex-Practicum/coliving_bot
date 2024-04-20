from rest_framework import serializers

from profiles.models import Coliving, Location, Profile, UserFromTelegram


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "name"]


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор объекта 'Profile'.
    """

    user = serializers.SlugRelatedField(slug_field="telegram_id", read_only=True)
    location = serializers.SlugRelatedField(
        queryset=Location.objects.all(), slug_field="name"
    )
    images = serializers.SlugRelatedField(
        slug_field="file_id", many=True, read_only=True
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
            "images",
        )


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
            "is_visible",
            "images",
        )


class UserResidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFromTelegram
        fields = ["residence"]


class RoommatesSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей с дополнительной информацией о возрасте и имени."""

    age = serializers.IntegerField(source="user_profile__age")
    name = serializers.CharField(source="user_profile__name")

    class Meta:
        model = UserFromTelegram
        fields = ["telegram_id", "name", "age"]
