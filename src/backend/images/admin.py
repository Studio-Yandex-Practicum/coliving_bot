from django.contrib import admin

from .models import ColivingImage, ProfileImage


@admin.register(ProfileImage)
class ProfileImageAdmin(admin.ModelAdmin):
    """
    Управление объектами 'ProfileImageAdmin' в админ-зоне.
    """

    list_display = ("id", "profile", "image", "file_id")


@admin.register(ColivingImage)
class ColivingImageAdmin(admin.ModelAdmin):
    """
    Управление объектами 'ColivingImage' в админ-зоне.
    """

    list_display = ("id", "coliving", "image", "file_id")
