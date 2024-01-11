from django.contrib import admin

from .models import MatchRequest, UserReport


@admin.register(MatchRequest)
class MatchRequestsAdmin(admin.ModelAdmin):
    """
    Управление объектами 'MatchRequests' в админ-зоне.
    """

    list_display = (
        "id",
        "sender",
        "receiver",
        "status",
        "created_date",
        "match_date",
    )


@admin.register(UserReport)
class UserReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "reporter",
        "reported_user",
        "text",
        "category",
        "status",
        "created_date",
    )
