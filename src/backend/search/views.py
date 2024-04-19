from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import exceptions, generics

from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from search.constants import MatchStatuses
from search.filters import ProfilesSearchFilterSet
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
    """
    Apiview для получения списка мэчтей.
    Параметр roomates запроса позволяет наложить
    дополнительный фильтр.
    roommates = 1 - выводим только тех пользователей,
    кто потенциально может стать соседом в коливинге,
    то есть помимо мэтча еще и не имеет своего коливинга
    и не проживает сейчас в коливинге

    roommates = 0 - выводим просто всех пользователей с мэтчем
    """

    serializer_class = MatchListSerializer

    def get_queryset(self):
        roommates = int(self.request.query_params.get("roommates", 0))

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
        matched_users = (users_who_sent_like | liked_users).distinct()

        if roommates == 1:
            matched_users = matched_users.filter(residence_id__isnull=True)
            matched_users = matched_users.select_related("residence").filter(
                coliving__host_id__isnull=True
            )
        return matched_users


class ProfilesSearchView(generics.ListAPIView):
    """Apiview для для поиска профилей."""

    queryset = Profile.objects.all().select_related("user", "location")
    serializer_class = ProfileSerializer
    filterset_class = ProfilesSearchFilterSet

    def get_queryset(self):
        try:
            user = UserFromTelegram.objects.get(
                telegram_id=self.request.query_params.get("viewer", None)
            )
        except ObjectDoesNotExist:
            raise exceptions.NotFound("Такого пользователя не существует.")
        excl_list = Profile.objects.filter(Q(user=user) | Q(viewers=user)).values_list(
            "pk", flat=True
        )
        return (
            super()
            .get_queryset()
            .filter(is_visible=True)
            .exclude(pk__in=excl_list)
            .order_by("pk")
        )


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
