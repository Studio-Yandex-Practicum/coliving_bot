from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q
from rest_framework import exceptions, generics, status
from rest_framework.generics import CreateAPIView, UpdateAPIView, get_object_or_404
from rest_framework.response import Response

from profiles.models import Coliving, Profile
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
        user_profile = get_object_or_404(
            Profile, user__telegram_id=self.kwargs.get("telegram_id")
        )
        liked_profiles = (
            user_profile.liked_profiles.filter(status=MatchStatuses.is_match)
            .annotate(
                telegram_id=F("receiver__user_id"),
                age=F("receiver__age"),
                name=F("receiver__name"),
            )
            .values("telegram_id", "age", "name")
        )
        received_likes = (
            user_profile.received_likes.filter(status=MatchStatuses.is_match)
            .annotate(
                telegram_id=F("sender__user_id"),
                age=F("sender__age"),
                name=F("sender__name"),
            )
            .values("telegram_id", "age", "name")
        )
        return liked_profiles.union(received_likes).all()


class ColivingLikesListAPIView(generics.ListAPIView):
    serializer_class = MatchedProfileSerializer

    def get_queryset(self):
        coliving = get_object_or_404(Coliving, pk=self.kwargs.get("pk"))
        likes = (
            coliving.likes.filter(status=MatchStatuses.is_match)
            .annotate(
                telegram_id=F("sender__user_id"),
                age=F("sender__age"),
                name=F("sender__name"),
            )
            .values("telegram_id", "age", "name")
        )
        return likes.all()


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
