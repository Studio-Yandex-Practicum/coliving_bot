from django.contrib import admin

from .models import Mailing


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """
    Управление объектами 'Mailing' в админ-зоне.
    """

    list_display = ("id", "text", "send_date", "image")
