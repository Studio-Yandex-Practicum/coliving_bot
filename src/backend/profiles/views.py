from rest_framework import generics
from .models import Coliving
from .serializers import ColivingSerializer
from .filtres import ColivingFilter
from django_filters.rest_framework import DjangoFilterBackend


class ColivingView(generics.ListCreateAPIView):
    """Apiview для создания и получения Coliving."""
    queryset = Coliving.objects.all()
    serializer_class = ColivingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ColivingFilter

    def get_queryset(self):
        queryset = Coliving.objects.all()
        owner = self.request.query_params.get('owner')
        if owner is not None:
            queryset = queryset.filter(host__telegram_id=owner)
        return queryset


class ColivingDetailView(generics.RetrieveUpdateAPIView):
    """Apiview для обновления Coliving."""
    queryset = Coliving.objects.all()
    serializer_class = ColivingSerializer
