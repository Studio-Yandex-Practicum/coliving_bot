from django.contrib import admin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import path, reverse
from django.utils.html import format_html

from profiles.models import Coliving
from search.constants import ACCEPT_REPORT_TEXT, REJECT_REPORT_TEXT, ReportStatuses
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
        "category",
        "status",
        "preview",
        "comment",
        "close_report",
    )
    list_filter = (
        "status",
        "category",
    )

    @admin.display(description="Закрыть жалобу")
    def close_report(self, obj):
        accept_url = reverse("admin:report-accept", args=[obj.id])
        reject_url = reverse("admin:report-reject", args=[obj.id])
        accept_style = "background-color:green;color:white"
        reject_style = "background-color:red;color:white"
        return format_html(
            """
            <a class="button" style="{accept_style}" href="{accept_url}">Принять</a>
            <a class="button" style="{reject_style}" href="{reject_url}">Отклонить</a>
            """,
            accept_style=accept_style,
            accept_url=accept_url,
            reject_style=reject_style,
            reject_url=reject_url,
        )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:report_id>/accept/",
                self.admin_site.admin_view(self.report_accept),
                name="report-accept",
            ),
            path(
                "<int:report_id>/reject/",
                self.admin_site.admin_view(self.report_reject),
                name="report-reject",
            ),
        ]
        return custom_urls + urls

    def report_accept(self, request, report_id):
        obj = get_object_or_404(UserReport, id=report_id)
        coliving = Coliving.objects.filter(host=obj.reported_user).first()

        obj.status = ReportStatuses.RESOLVED
        obj.save()

        obj.reported_user.is_banned = True
        obj.reported_user.save()

        obj.reported_user.residence_id = None
        obj.reported_user.save()

        obj.reported_user.user_profile.is_visible = False
        obj.reported_user.user_profile.save()

        if coliving:
            coliving.is_visible = False
            coliving.save()

        profile = obj.reported_user.user_profile

        ProfileLike.objects.filter(Q(sender=profile) | Q(receiver=profile)).delete()
        ColivingLike.objects.filter(Q(sender=profile) | Q(coliving=coliving)).delete()

        self.message_user(
            request, ACCEPT_REPORT_TEXT.format(username=obj.reported_user)
        )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    def report_reject(self, request, report_id):
        obj = get_object_or_404(UserReport, id=report_id)

        obj.status = ReportStatuses.REJECTED
        obj.save()

        self.message_user(request, REJECT_REPORT_TEXT)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    def change_view(self, request, object_id, form_url="", extra_context=None):
        obj = get_object_or_404(UserReport, pk=object_id)

        if obj.status == ReportStatuses.RECEIVED:
            obj.status = ReportStatuses.VIEWED
            obj.save()

        return super().change_view(request, object_id, form_url, extra_context)

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
                """
                <div>
                  <a href="{img_url}" target="_blank">
                    <img src="{img_url}"
                         style="max-height: 200px; transition: max-height 0.3s ease;"
                         onclick="this.style.maxHeight = this.style.maxHeight ==
                                        '500px' ? '200px' : '500px'; return false;" />
                  </a>
                  <div style="margin-top: 5px;">
                    <a href="{img_url}" target="_blank" class="button"
                                             style="display: block;">Полный размер</a>
                  </div>
                </div>
                """,
                img_url=img_url,
            )
        return "Нет скриншотов"
