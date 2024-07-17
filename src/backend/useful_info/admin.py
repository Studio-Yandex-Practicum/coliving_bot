from django.contrib import admin

from useful_info.models import UsefulMaterial


@admin.register(UsefulMaterial)
class UsefulMaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "file", "link")
    search_fields = ("title",)
