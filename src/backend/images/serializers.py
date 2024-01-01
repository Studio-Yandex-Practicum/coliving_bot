from rest_framework import serializers

from .models import ColivingImage, ProfileImage


class BaseImageSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор объектов 'ProfileImage', 'ColivingImage'.
    """

    class Meta:
        fields = ("file_id", "image")
        read_only_fields = fields


class ProfileImageReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор объекта 'ProfileImage' (безопасные методы).
    """

    class Meta(BaseImageSerializer.Meta):
        model = ProfileImage


class ProfileImageCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор объекта 'ProfileImage' (небезопасные методы).
    """

    class Meta(ProfileImageReadSerializer.Meta):
        read_only_fields = ("profile",)


class ColivingImageReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор объекта 'ColivingImage' (безопасные методы).
    """

    class Meta(BaseImageSerializer.Meta):
        model = ColivingImage


class ColivingImageCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор объекта 'ColivingImage' (небезопасные методы).
    """

    class Meta(ColivingImageReadSerializer.Meta):
        read_only_fields = ("coliving",)
