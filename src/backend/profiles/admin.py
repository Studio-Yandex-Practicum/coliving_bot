from django.contrib import admin

from .models import Coliving, Profile, Location, UserFromTelegram


@admin.register(UserFromTelegram)
class UserFromTelegramAdmin(admin.ModelAdmin):
    """
        Управление объектами 'UserFromTelegram' в админ-зоне.
    """

    list_display = ('id', 'telegram_id', 'residence')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """
        Управление объектами 'Location' в админ-зоне.
    """

    list_display = ('id', 'name')


class RoommatesInline(admin.TabularInline):
    """
        Презентация объектов 'UserFromTelegram' на странице коливинга.
    """

    model = UserFromTelegram


@admin.register(Coliving)
class ColivingAdmin(admin.ModelAdmin):
    """
        Управление объектами 'Coliving' в админ-зоне.
    """

    list_display = (
        'id', 'host', 'location', 'price', 'room_type', 'about', 'is_visible',
        'created_date',
    )
    inlines = (RoommatesInline,)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
        Управление объектами 'Profile' в админ-зоне.
    """

    list_display = (
        'id', 'user', 'name', 'sex', 'age', 'location', 'about', 'is_visible',
        'created_date',
    )
