from django.urls import path

from .views import ColivingView, ColivingDetailView


urlpatterns = [
    path('v1/colivings/', ColivingView.as_view()),
    path('v1/colivings/<int:pk>/', ColivingDetailView.as_view()),
]
