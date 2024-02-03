from rest_framework import exceptions, generics

from search.constants import MatchStatuses
from search.models import MatchRequest, UserFromTelegram, UserReport
from search.serializers import (
    MatchListSerializer,
    MatchRequestSerializer,
    UserReportSerializer,
)


class UserReportCreateView(generics.CreateAPIView):
    """Apiview для создания жалобы."""

    queryset = UserReport.objects.all()
    serializer_class = UserReportSerializer


class MatchedUsersListView(generics.ListAPIView):
    """Apiview для получения списка мэчтей."""

    serializer_class = MatchListSerializer

    def get_queryset(self):
        telegram_id = self.kwargs.get("telegram_id")
        user = UserFromTelegram.objects.filter(telegram_id=telegram_id).first()
        if user is None:
            raise exceptions.NotFound("Такого пользователя не существует.")
        users_who_sent_like = UserFromTelegram.objects.select_related(
            "user_profile"
        ).filter(
            likes__receiver=user,
            likes__status=MatchStatuses.is_match,
        )
        liked_users = UserFromTelegram.objects.select_related("user_profile").filter(
            match_requests__sender=user,
            match_requests__status=MatchStatuses.is_match,
        )
        return (users_who_sent_like | liked_users).all()


class MatchRequestView(generics.CreateAPIView):
    """Apiview для создания MatchRequest."""
    queryset = MatchRequest.objects.all()
    serializer_class = MatchRequestSerializer

    def perform_create(self, serializer):
        user = self.request.data.get("sender")
        user_1 = self.request.data.get("receiver")
        math = MatchRequest.objects.filter(
            sender__telegram_id=user_1,
            receiver__telegram_id=user)
        if math:
            math.update(status=MatchStatuses.is_match)
        else:
            return serializer.save()
