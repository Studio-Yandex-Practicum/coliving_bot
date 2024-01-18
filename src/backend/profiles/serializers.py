from rest_framework import serializers

from .models import Profile


class ProfileCreateSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    location = serializers.CharField()

    class Meta:
        model = Profile
        fields = (
            "user", "name", "sex", "age", "location", "about", "is_visible",)

    def to_internal_value(self, data):
        location_name = data.get("location")
        data["location"] = location_name
        return super().to_internal_value(data)

    def get_user(self, obj):
        telegram_id = self.context["request"].parser_context["kwargs"]["telegram_id"]
        return telegram_id


class ProfileReadSerializer(serializers.ModelSerializer):
    pass
