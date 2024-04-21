from django.contrib import admin

from images.models import ColivingImage, ProfileImage
from profiles.models import Coliving, Location, Profile, UserFromTelegram


@admin.register(UserFromTelegram)
class UserFromTelegramAdmin(admin.ModelAdmin):
    """
    Управление объектами 'UserFromTelegram' в админ-зоне.
    """

    list_display = ("id", "telegram_id", "residence")
    list_editable = ("residence",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """
    Управление объектами 'Location' в админ-зоне.
    """

    list_display = ("id", "name")


class ProfileImagesInline(admin.TabularInline):
    """
    Отображение объектов 'ProfileImage' на странице профиля.
    """

    model = ProfileImage


class ColivingImagesInline(admin.TabularInline):
    """
    Отображение объектов 'ColivingImage' на странице коливинга.
    """

    model = ColivingImage


class RoommatesInline(admin.TabularInline):
    """
    Отображение объектов 'UserFromTelegram' на странице коливинга (соседи по коливингу).
    """

    model = UserFromTelegram


@admin.register(Coliving)
class ColivingAdmin(admin.ModelAdmin):
    """
    Управление объектами 'Coliving' в админ-зоне.
    """

    list_display = (
        "id",
        "host",
        "location",
        "price",
        "room_type",
        "about",
        "is_visible",
        "created_date",
    )
    inlines = (RoommatesInline, ColivingImagesInline)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Управление объектами 'Profile' в админ-зоне.
    """

    list_display = (
        "id",
        "user",
        "name",
        "sex",
        "age",
        "location",
        "about",
        "is_visible",
        "created_date",
    )
    inlines = (ProfileImagesInline,)
