from django.urls import path

from .views import LocationList

urlpatterns = [
    path('v1/locations/', LocationList.as_view(), name='location-list'),
]
