from rest_framework import exceptions, generics

from search.models import UserFromTelegram, UserReport
from search.serializers import MatchListSerializer, UserReportSerializer


class UserReportCreateView(generics.CreateAPIView):
    """Apiview для создания жалобы."""

    queryset = UserReport.objects.all()
    serializer_class = UserReportSerializer


class MatchedUsersListView(generics.ListAPIView):
    """Apiview для получения списка мэчтей."""

    serializer_class = MatchListSerializer

    def get_queryset(self):
        telegram_id = self.kwargs.get("telegram_id")
        if not UserFromTelegram.objects.filter(telegram_id=telegram_id).exists():
            raise exceptions.NotFound("Такого пользователя не существует.")
        return UserFromTelegram.objects.filter(
            likes__receiver__telegram_id=telegram_id,
            match_requests__sender__telegram_id=telegram_id,
            match_requests__status=1,
        ).distinct()
