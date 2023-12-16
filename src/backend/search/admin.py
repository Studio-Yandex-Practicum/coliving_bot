from django.contrib import admin

from .models import MatchRequest


@admin.register(MatchRequest)
class MatchRequestsAdmin(admin.ModelAdmin):
    """
        Управление объектами 'MatchRequests' в админ-зоне.
    """

    list_display = (
        'id', 'sender', 'receiver', 'status', 'created_date',
        'match_date'
    )
