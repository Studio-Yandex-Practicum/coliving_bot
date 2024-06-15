from django.utils.timezone import now
from rest_framework import mixins, viewsets

from profiles.models import UserFromTelegram

from .filters import UsersResultsSetPagination
from .models import Mailing
from .serializers import MailingSerializer, UserMailSerializer


class MailingView(
    mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    """
    Apiview для модели Mailing.
    """

    serializer_class = MailingSerializer

    def get_queryset(self):
        current_datetime = now()
        queryset = Mailing.objects.filter(
            send_date__lte=current_datetime, is_sent="is_waiting"
        )
        return queryset


class UserMailView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Apiview для модели UserFromTelegram для получения списка пользователей.
    """

    queryset = UserFromTelegram.objects.all()
    serializer_class = UserMailSerializer
    pagination_class = UsersResultsSetPagination
