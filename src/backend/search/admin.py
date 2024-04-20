from django.contrib import admin

from search.models import ColivingLike, ProfileLike, UserReport


@admin.register(ProfileLike)
class ProfileLikeAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "status", "match_date", "created_date")
    list_filter = ("status",)
    readonly_fields = ("created_date", "match_date")


@admin.register(ColivingLike)
class ColivingLikeAdmin(admin.ModelAdmin):
    list_display = ("sender", "coliving", "status", "match_date", "created_date")
    list_filter = ("status",)
    readonly_fields = ("created_date", "match_date")


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
