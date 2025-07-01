from django.contrib import admin
from doc.models import Letters, Organizations, Disk, Type, Okr, Peoples
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rangefilter.filters import DateRangeFilter
admin.site.site_header = "Учетик НИЛ-103"
admin.site.site_title = "Панель управления"
admin.site.index_title = "Добро пожаловать в админку"


@admin.register(Letters)
class LettersAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "type",
        "formated_addressees",
        "okr",
        "formated_content",
        "send_date",
        "formated_linked_disks",
        "author",

    )
    search_fields = ("number", "content")
    list_filter = (
        "addressee",
        "type",
        "okr",
        "author",
        "workers",
        ("send_date", DateRangeFilter),
    )

    @admin.display(description="Диски")
    def formated_linked_disks(self, obj):
        links = []
        for disk in obj.disk.all():
            url = reverse("admin:doc_disk_change", args=[disk.pk])
            links.append(f'<a href="{url}">{disk.number}</a>')
        return format_html("\n".join(links))

    @admin.display(description="Адресаты")
    def formated_addressees(self, obj):
        return format_html("<br>".join([org.name for org in obj.addressee.all()]))

    @admin.display(description="Содержание")
    def formated_content(self, obj):
        return (
            (obj.content[:25] + obj.content[25:50] + "...")
            if len(obj.content) > 50
            else obj.content
        )

    def save_model(self, request, obj, form, change):
        if not change or not obj.author:
            obj.author = request.user
        obj.save()


@admin.register(Organizations)
class OrganizationsAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Disk)
class DiskAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "copyes",
        "content",
    )

    search_fields = ("number",)
    list_filter = ("number",)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ("type",)
    search_fields = ("type",)
    list_filter = ("type",)


@admin.register(Okr)
class OkrAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Peoples)
class PeoplesAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)
