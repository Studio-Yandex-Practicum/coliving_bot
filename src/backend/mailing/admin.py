from django.contrib import admin

from .models import Mailing


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """
    Управление объектами 'Mailing' в админ-зоне.
    """

    list_display = ("id", "text", "send_date", "image", "status")
    list_display_links = ("id", "text")
    list_filter = ("status",)
    date_hierarchy = "send_date"
