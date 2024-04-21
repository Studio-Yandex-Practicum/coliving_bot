from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import exceptions, generics, status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response

from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from search.constants import MatchStatuses
from search.filters import ProfilesSearchFilterSet
from search.models import ColivingLike, ProfileLike, UserFromTelegram, UserReport
from search.serializers import (
    ColivingLikeCreateSerializer,
    ColivingLikeUpdateSerializer,
    MatchedProfileSerializer,
    ProfileLikeCreateSerializer,
    ProfileLikeUpdateSerializer,
    UserReportSerializer,
)


class UserReportCreateView(generics.CreateAPIView):
    """Apiview для создания жалобы."""

    queryset = UserReport.objects.all()
    serializer_class = UserReportSerializer


class MatchedProfileListAPIView(generics.ListAPIView):
    serializer_class = MatchedProfileSerializer

    def get_queryset(self):
        telegram_id = self.kwargs.get("telegram_id")
        user = Profile.objects.filter(user__telegram_id=telegram_id).first()
        if not user:
            raise exceptions.NotFound("Такого пользователя не существует.")
        liked_profiles = user.liked_profiles.filter(status=MatchStatuses.is_match)
        received_likes = user.received_likes.filter(status=MatchStatuses.is_match)
        return (liked_profiles | received_likes).values("age", "name").all()


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


class ProfileLikeCreateAPIView(CreateAPIView):
    queryset = ProfileLike.objects.all()
    serializer_class = ProfileLikeCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sender = serializer.validated_data["sender"]
        receiver = serializer.validated_data["receiver"]

        reverse_like = ProfileLike.objects.filter(
            sender=receiver, receiver=sender
        ).first()
        if reverse_like:
            reverse_like.status = MatchStatuses.is_match
            reverse_like.save()
            return Response(
                ProfileLikeCreateSerializer(reverse_like).data,
                status=status.HTTP_200_OK,
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ProfileLikeUpdateAPIView(UpdateAPIView):
    queryset = ProfileLike.objects.all()
    serializer_class = ProfileLikeUpdateSerializer

    @property
    def allowed_methods(self):
        result = super().allowed_methods
        result.remove("PUT")
        return result


class ColivingLikeCreateAPIView(CreateAPIView):
    queryset = ColivingLike.objects.all()
    serializer_class = ColivingLikeCreateSerializer


class ColivingLikeUpdateAPIView(UpdateAPIView):
    queryset = ColivingLike.objects.all()
    serializer_class = ColivingLikeUpdateSerializer

    @property
    def allowed_methods(self):
        result = super().allowed_methods
        result.remove("PUT")
        return result
