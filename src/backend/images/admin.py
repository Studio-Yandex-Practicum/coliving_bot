from django.contrib import admin

from profiles.models import Coliving, Profile, Location, UserFromTelegram


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


@admin.register(Coliving)
class ColivingAdmin(admin.ModelAdmin):
    """
        Управление объектами 'Coliving' в админ-зоне.
    """

    list_display = (
        'id', 'host', 'location', 'price', 'room_type', 'about', 'is_visible',
        'created_date',
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
        Управление объектами 'Profile' в админ-зоне.
    """

    list_display = (
        'id', 'user', 'name', 'sex', 'age', 'location', 'about', 'is_visible',
        'created_date',
    )
