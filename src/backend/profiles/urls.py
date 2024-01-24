from django.urls import path

from .views import LocationList

app_name = 'api-v1'
urlpatterns = [
    path('v1/locations/', LocationList.as_view(), name='location-list'),
]
