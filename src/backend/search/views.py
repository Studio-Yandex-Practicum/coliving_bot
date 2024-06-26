from django.db.models import F, Q
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView, UpdateAPIView, get_object_or_404
from rest_framework.response import Response

from profiles.models import Coliving, Profile
from profiles.serializers import ProfileSerializer
from search.constants import ALREADY_REPORTED, MatchStatuses
from search.filters import ProfilesSearchFilterSet
from search.models import ColivingLike, ProfileLike, UserReport
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

    def create(self, request, *args, **kwargs):
        reporter = request.data.get("reporter")
        reported_user = request.data.get("reported_user")

        if UserReport.objects.filter(
            reporter=reporter, reported_user=reported_user
        ).exists():
            return Response(
                {"detail": ALREADY_REPORTED}, status=status.HTTP_208_ALREADY_REPORTED
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class MatchedProfileListAPIView(generics.ListAPIView):
    serializer_class = MatchedProfileSerializer

    def get_queryset(self):
        user_profile = get_object_or_404(
            Profile, user__telegram_id=self.kwargs.get("telegram_id")
        )
        sent_likes = (
            user_profile.sent_likes.filter(status=MatchStatuses.is_match)
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
        return sent_likes.union(received_likes).all()


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


class PotentialRoommatesListAPIView(generics.ListAPIView):
    queryset = Profile.objects.select_related("location", "user").prefetch_related(
        "images"
    )
    serializer_class = ProfileSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        coliving = get_object_or_404(Coliving, pk=self.kwargs.get("pk"))
        user_profile = coliving.host.user_profile
        coliving_ids = coliving.likes.filter(
            status=MatchStatuses.is_match,
        ).values_list("sender__id", flat=True)
        sent_like_ids = user_profile.sent_likes.filter(
            status=MatchStatuses.is_match,
        ).values_list("receiver__id", flat=True)
        received_like_ids = user_profile.received_likes.filter(
            status=MatchStatuses.is_match,
        ).values_list("sender__id", flat=True)
        return (
            queryset.filter(
                Q(id__in=coliving_ids)
                | Q(id__in=sent_like_ids)
                | Q(id__in=received_like_ids)
            )
            .exclude(id=user_profile.id)
            .filter(is_visible=True)
            .order_by("pk")
            .all()
        )


class ProfilesSearchView(generics.ListAPIView):
    """Apiview для для поиска профилей."""

    queryset = Profile.objects.select_related("location", "user").prefetch_related(
        "images"
    )

    serializer_class = ProfileSerializer
    filterset_class = ProfilesSearchFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()
        viewer = self.request.query_params.get("viewer")
        if viewer is None:
            return queryset.all()
        user_profile = get_object_or_404(Profile, user_id=viewer)
        return (
            queryset.exclude(
                id__in=user_profile.sent_likes.values_list(
                    "receiver__id",
                    flat=True,
                ),
            )
            .exclude(
                id__in=user_profile.received_likes.values_list(
                    "sender__id",
                    flat=True,
                ),
            )
            .exclude(id=user_profile.id)
            .filter(is_visible=True)
            .order_by("pk")
            .all()
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
