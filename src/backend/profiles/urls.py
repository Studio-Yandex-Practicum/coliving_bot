from django.urls import path

from .views import ColivingDetailView, ColivingView

app_name = "api-v1"

urlpatterns = [
    path('v1/colivings/', ColivingView.as_view(), name="colivings"),
    path('v1/colivings/<int:pk>/', ColivingDetailView.as_view(), name="coliving_id"),
]
