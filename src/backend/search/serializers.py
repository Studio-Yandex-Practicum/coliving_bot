from rest_framework import serializers

from profiles.models import Profile, UserFromTelegram
from search.models import ColivingLike, ProfileLike, UserReport


class UserReportImageSerializer(serializers.ImageField):
    """
    Сериализатор для обработки изображений в жалобах.
    """

    def to_internal_value(self, data):
        return super().to_internal_value(data)

    def to_representation(self, value):
        return value.url if value else None


class UserReportSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания жалоб.
    """

    reporter = serializers.SlugRelatedField(
        slug_field="telegram_id", queryset=UserFromTelegram.objects.all()
    )
    reported_user = serializers.SlugRelatedField(
        slug_field="telegram_id", queryset=UserFromTelegram.objects.all()
    )
    screenshot = UserReportImageSerializer(required=False, allow_null=True)

    class Meta:
        model = UserReport
        fields = ("reporter", "reported_user", "text", "category", "screenshot")
        extra_kwargs = {
            "text": {"required": False, "allow_blank": True},
            "category": {"required": True},
        }


class MatchedProfileSerializer(serializers.Serializer):
    """Сериализатор для получения списка мэтчей."""

    telegram_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)


class ProfileLikeCreateSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(
        slug_field="user_id",
        queryset=Profile.objects.all(),
    )
    receiver = serializers.SlugRelatedField(
        slug_field="user_id",
        queryset=Profile.objects.all(),
    )

    class Meta:
        model = ProfileLike
        fields = ("id", "sender", "receiver", "status")
        read_only_fields = ("id",)


class ProfileLikeUpdateSerializer(ProfileLikeCreateSerializer):
    class Meta:
        model = ProfileLike
        fields = ("id", "sender", "receiver", "status")
        read_only_fields = ("id", "sender", "receiver")


class ColivingLikeCreateSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(
        slug_field="user_id", queryset=Profile.objects.all()
    )

    class Meta:
        model = ColivingLike
        fields = ("id", "sender", "coliving", "status")
        read_only_fields = ("id",)


class ColivingLikeUpdateSerializer(ColivingLikeCreateSerializer):
    class Meta:
        model = ColivingLike
        fields = ("id", "sender", "coliving", "status")
        read_only_fields = ("id", "sender", "coliving")
