from rest_framework import serializers

from profiles.models import UserFromTelegram
from search.models import MatchRequest, UserReport


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


class MatchListSerializer(serializers.ModelSerializer):
    """Сериализатор для получения списка мэтчей."""

    name = serializers.CharField(read_only=True, source="user_profile.name")
    age = serializers.IntegerField(read_only=True, source="user_profile.age")

    class Meta:
        model = UserFromTelegram
        fields = ("telegram_id", "name", "age")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        profile = getattr(instance, "user_profile")
        representation["name"] = profile.name
        representation["age"] = profile.age
        return representation


class MatchRequestSerializer(serializers.ModelSerializer):
    """Сериализатор для создания MatchRequest."""

    receiver = serializers.SlugRelatedField(
        slug_field="telegram_id", queryset=UserFromTelegram.objects.all()
    )
    sender = serializers.SlugRelatedField(
        slug_field="telegram_id", queryset=UserFromTelegram.objects.all()
    )

    class Meta:
        model = MatchRequest
        fields = ("id", "receiver", "sender", "status")
        read_only_fields = ("id",)
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=MatchRequest.objects.all(),
                fields=("sender", "receiver"),
                message="Запрос MatchRequest уже создан.",
            )
        ]


class MatchRequestUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления статуса MatchRequest."""

    class Meta:
        model = MatchRequest
        fields = ("receiver", "sender", "status")
        read_only_fields = ("id", "receiver", "sender")
