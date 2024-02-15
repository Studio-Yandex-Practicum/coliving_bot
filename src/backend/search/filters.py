from django_filters import FilterSet, ModelChoiceFilter, RangeFilter

from profiles.models import Profile, Location

class ProfilesSearchFilterSet(FilterSet):
    location = ModelChoiceFilter(field_name='location',
                                 queryset=Location.objects.all())
    sex = ModelChoiceFilter(field_name='sex')
    age = RangeFilter(field_name='age')

    class Meta:
        model = Profile
        fields = ['location', 'sex', 'age']
