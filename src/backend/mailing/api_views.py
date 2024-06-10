from rest_framework import mixins, viewsets

from profiles.filters import SmallResultsSetPagination
from profiles.models import UserFromTelegram

from .models import Mailing
from .serializers import MailingSerializer, UserMailSerializer


class MailingView(
    mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    """
    Apiview для модели Mailing.
    """

    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class UserMailView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Apiview для модели UserFromTelegram для получения списка пользователей.
    """

    queryset = UserFromTelegram.objects.all()
    serializer_class = UserMailSerializer
    pagination_class = SmallResultsSetPagination
