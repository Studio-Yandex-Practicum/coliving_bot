from rest_framework import exceptions, generics, status, viewsets
from rest_framework.response import Response

from search.constants import MatchStatuses

from profiles.serializers import ProfileSerializer
from profiles.constants import Sex, ColivingTypes
from profiles.models import Profile, Location

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

        return (users_who_sent_like | liked_users).distinct()


class ProfilesSearchView(generics.ListAPIView):
    """Apiview для для поиска профилей."""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        user = UserFromTelegram.objects.get(
            telegram_id=request.query_params.get("telegram_id", None))
        if user is None:
            raise exceptions.NotFound("Такого пользователя не существует.")
        age_lt = request.query_params.get("age_lt", None) 
        age_gte = request.query_params.get("age_gte", None) 
        sex = request.query_params.get("sex", None)
        sex = Sex.MAN if sex == "Парень" else Sex.WOMAN
        location = Location.objects.filter(
            name=request.query_params.get("location", None)).first()

        serializer = self.get_serializer(
            self.get_queryset().filter(
                    sex=sex).filter(
                    location=location.pk).filter(
                    age__gte=age_gte).filter(
                    age__lt=age_lt).order_by("-created_date"),
                    many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MatchRequestView(generics.CreateAPIView):
    """Apiview для создания MatchRequest."""

    queryset = MatchRequest.objects.all()
    serializer_class = MatchRequestSerializer

    def perform_create(self, serializer):
        sender = self.request.data.get("sender")
        receiver = self.request.data.get("receiver")
        match = MatchRequest.objects.filter(
            sender__telegram_id=receiver, receiver__telegram_id=sender
        )
        if match:
            match.update(status=MatchStatuses.is_match)
        else:
            return serializer.save()
