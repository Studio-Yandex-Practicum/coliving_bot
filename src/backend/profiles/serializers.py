from rest_framework import serializers

from profiles.models import Location, Profile


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
