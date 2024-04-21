from django_filters import ChoiceFilter, FilterSet, ModelChoiceFilter, RangeFilter

from profiles.constants import Sex
from profiles.models import Location, Profile
from search.models import MatchRequest


class ProfilesSearchFilterSet(FilterSet):
    location = ModelChoiceFilter(
        field_name="location__name",
        to_field_name="name",
        queryset=Location.objects.all(),
    )
    sex = ChoiceFilter(field_name="sex", choices=Sex.choices)
    age = RangeFilter(field_name="age")

    class Meta:
        model = Profile
        fields = ["location", "sex", "age"]


class MatchRequestFilter(FilterSet):
    class Meta:
        model = MatchRequest
        fields = (
            "sender__telegram_id",
            "receiver__telegram_id",
        )
