from django_filters import rest_framework as filters

from profiles.models import Coliving


class ColivingFilter(filters.FilterSet):
    """
    Фильтрация Coliving.
    """

    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    location = filters.CharFilter(field_name="location__name")
    owner = filters.NumberFilter(field_name="host__telegram_id")

    class Meta:
        model = Coliving
        fields = (
            "location",
            "room_type",
            "min_price",
            "max_price",
            "owner",
        )
