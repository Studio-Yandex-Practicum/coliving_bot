from rest_framework import serializers

from .models import ColivingImage, ProfileImage


class ProfileImageReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор объекта 'ProfileImage' (безопасные методы).
    """

    class Meta:
        model = ProfileImage
        fields = ("file_id", "profile", "image")
        read_only_fields = fields


class ProfileImageCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор объекта 'ProfileImage' (небезопасные методы).
    """

    class Meta:
        model = ProfileImage
        fields = ("file_id", "profile", "image")
        read_only_fields = ("profile",)


class ColivingImageReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор объекта 'ColivingImage' (безопасные методы).
    """

    class Meta:
        model = ColivingImage
        fields = ("file_id", "coliving")
        read_only_fields = fields
