from django_filters import FilterSet, ModelChoiceFilter

from profiles.models import Profile, Location

class ProfilesSearchFilterSet(FilterSet):
    location = ModelChoiceFilter(field_name='location',
                                 queryset=Location.objects.all())
    sex = ModelChoiceFilter(field_name='sex')

    class Meta:
        model = Profile
        fields = ['location', 'sex', 'age']
