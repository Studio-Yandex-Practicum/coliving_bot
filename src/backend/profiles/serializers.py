from rest_framework import serializers

from .models import Location, Profile


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

    def get_user(self, obj):
        telegram_id = self.context["request"].parser_context["kwargs"]["telegram_id"]
        return telegram_id
