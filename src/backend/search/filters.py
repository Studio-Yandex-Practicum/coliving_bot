from django_filters import ChoiceFilter, FilterSet, ModelChoiceFilter, RangeFilter

from profiles.models import Location, Profile
from profiles.constants import Sex


class ProfilesSearchFilterSet(FilterSet):
    location = ModelChoiceFilter(field_name='location',
                                 queryset=Location.objects.all())
    sex = ChoiceFilter(field_name='sex', choices=Sex.choices)
    age = RangeFilter(field_name='age')

    class Meta:
        model = Profile
        fields = ['location', 'sex', 'age']
