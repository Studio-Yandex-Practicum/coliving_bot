from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .filtres import ColivingFilter
from .models import Coliving
from .serializers import ColivingSerializer


class ColivingView(generics.ListCreateAPIView):
    """Apiview для создания и получения Coliving."""
    queryset = Coliving.objects.all()
    serializer_class = ColivingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ColivingFilter


class ColivingDetailView(generics.RetrieveUpdateAPIView):
    """Apiview для обновления Coliving."""
    queryset = Coliving.objects.all()
    serializer_class = ColivingSerializer
