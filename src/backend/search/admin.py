from django.contrib import admin
from django.utils.html import format_html

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
    date_hierarchy = "created_date"
    list_display = (
        "id",
        "reporter",
        "reported_user",
        "category",
        "status",
        "created_date",
        "comment",
    )
    exclude = ("screenshot", "text")
    readonly_fields = (
        "reporter",
        "reported_user",
        "preview",
        "comment",
    )
    list_filter = (
        "status",
        "category",
    )

    @admin.display(description="Комментарий")
    def comment(self, obj):
        if obj.text:
            return obj.text
        return "Пользователь не отправил комментарий."

    @admin.display(description="Скриншот")
    def preview(self, obj):
        if obj.screenshot:
            img_url = obj.screenshot.url
            return format_html(
                f"<div>"
                f'<a href="{img_url}" target="_blank" onclick="return false;">'
                f'<img src="{img_url}" style="max-height: 200px; '
                f'transition: max-height 0.3s ease;" '
                f'onclick="'
                f"this.style.maxHeight=this.style.maxHeight=='500px'?'200px':'500px'; "
                f'return false;" />'
                f"</a>"
                f'<div style="margin-top: 5px;">'
                f'<a href="{img_url}" target="_blank" class="button" '
                f'style="display: block;">Полный размер</a>'
                f"</div>"
                f"</div>"
            )
        return "Нет скриншотов"
