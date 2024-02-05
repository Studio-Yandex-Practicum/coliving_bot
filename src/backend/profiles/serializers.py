from rest_framework import serializers

from profiles.models import Location, Profile


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
