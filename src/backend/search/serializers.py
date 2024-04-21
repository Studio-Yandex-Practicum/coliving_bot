from rest_framework import serializers

from profiles.models import Profile, UserFromTelegram
from search.models import ColivingLike, ProfileLike, UserReport


class UserReportSerializer(serializers.ModelSerializer):
    """Сериализатор для создания жалоб."""

    reporter = serializers.SlugRelatedField(
        slug_field="telegram_id", queryset=UserFromTelegram.objects.all()
    )
    reported_user = serializers.SlugRelatedField(
        slug_field="telegram_id", queryset=UserFromTelegram.objects.all()
    )

    class Meta:
        model = UserReport
        fields = ("reporter", "reported_user", "text", "category")
        extra_kwargs = {
            "text": {"required": True},
            "category": {"required": True},
        }


class MatchedProfileSerializer(serializers.Serializer):
    """Сериализатор для получения списка мэтчей."""

    telegram_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)


class OnlyLikeStatusWriteSerializerMixin:
    class Meta:
        model = ProfileLike
        fields = ("status", "id", "sender", "receiver", "match_date", "created_date")
        read_only_fields = ("id", "sender", "receiver", "match_date", "created_date")


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
        fields = ("id", "sender", "receiver", "status", "match_date", "created_date")
        read_only_fields = ("id", "match_date", "created_date")


class ProfileLikeUpdateSerializer(
    OnlyLikeStatusWriteSerializerMixin, ProfileLikeCreateSerializer
):
    pass


class ColivingLikeCreateSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(
        slug_field="user_id", queryset=Profile.objects.all()
    )

    class Meta:
        model = ColivingLike
        fields = ("id", "sender", "coliving", "status", "match_date", "created_date")
        read_only_fields = ("id", "match_date", "created_date")


class ColivingLikeUpdateSerializer(
    OnlyLikeStatusWriteSerializerMixin, ColivingLikeCreateSerializer
):
    pass