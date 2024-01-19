from rest_framework import serializers

from .models import Location, Profile


class ProfileReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор объекта 'Profile' (безопасные методы).
    """

    user = serializers.SerializerMethodField()

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

    def get_user(self, obj):
        telegram_id = self.context["request"].parser_context["kwargs"]["telegram_id"]
        return telegram_id


class ProfileCreateSerializer(ProfileReadSerializer):
    """
    Сериализатор объекта 'Profile' (создание объекта).
    """

    location = serializers.CharField()

    def to_internal_value(self, data):
        location_name = data.get("location")
        data["location"] = location_name
        return super().to_internal_value(data)


class ProfileUpdateSerializer(ProfileReadSerializer):
    """
    Сериализатор объекта 'Profile' (обновление объекта).
    """

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        location_id = representation.get("location")
        if location_id is not None:
            location = Location.objects.filter(id=location_id).first()
            if location:
                representation["location"] = location.name
        return representation
