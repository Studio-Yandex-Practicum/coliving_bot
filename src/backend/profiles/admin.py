from django.contrib import admin
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html

from images.models import ColivingImage, ProfileImage
from profiles.models import Coliving, Location, Profile, UserFromTelegram
from search.models import ColivingLike, ProfileLike


@admin.register(UserFromTelegram)
class UserFromTelegramAdmin(admin.ModelAdmin):
    """
    Управление объектами 'UserFromTelegram' в админ-зоне.
    """

    list_display = ("telegram_id", "residence", "is_banned")
    list_filter = ("is_banned",)
    search_fields = ("telegram_id",)
    readonly_fields = (
        "telegram_id",
        "user_profile",
        "residence",
        "coliving",
    )

    def user_profile(self, obj):
        return obj.user_profile

    def save_model(self, request, obj, form, change):
        if obj.is_banned:
            obj.user_profile.is_visible = False
            obj.user_profile.save()

            obj.residence_id = None
            obj.save()

            coliving = Coliving.objects.filter(host=obj).first()

            if coliving:
                coliving.is_visible = False
                coliving.save()

            profile = obj.user_profile
            ProfileLike.objects.filter(Q(sender=profile) | Q(receiver=profile)).delete()
            ColivingLike.objects.filter(
                Q(sender=profile) | Q(coliving=coliving)
            ).delete()

        super().save_model(request, obj, form, change)

    @admin.display(description="Владелец коливинга")
    def coliving(self, obj):
        coliving = Coliving.objects.filter(host=obj).first()
        if coliving:
            url = reverse("admin:profiles_coliving_change", args=[coliving.id])
            return format_html('<a href="{}">Коливинг {}</a>', url, coliving.id)
        return "У пользователя нет своих коливингов."


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
