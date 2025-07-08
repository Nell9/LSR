from django.contrib import admin
from rangefilter.filters import DateRangeFilter
from django import forms
from .models import (
    topics,
    Organizations,
    Disk,
    Memo,
    Act,
    OutgoingLetter,
    IncomingLetter,
    AttachedFile,  # Letters
)
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.admin import GenericTabularInline

User = get_user_model()
admin.site.site_header = "Учетик НИЛ-103"
admin.site.site_title = "Панель управления"
admin.site.index_title = "Добро пожаловать в админку"
# Общий миксин для Document-наследников, чтобы не дублировать код


class AttachedFileInline(GenericTabularInline):
    model = AttachedFile
    extra = 1
    max_num = 10
    verbose_name = "Прикрепленный документ"
    verbose_name_plural = "Прикрепленные документы"


class DocumentAdminMixin(admin.ModelAdmin):
    readonly_fields = ("author",)  # сделаем поле только для чтения
    ordering = ("self_date",)

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_topics(self, obj):
        return ", ".join([org.name for org in obj.topic.all()])

    get_topics.short_description = "Темы"


@admin.register(topics)
class TopicsAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Organizations)
class OrganizationsAdmin(admin.ModelAdmin):
    list_display = ("name", "addressee", "head")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Disk)
class DiskAdmin(admin.ModelAdmin):
    list_display = ("number", "copyes", "content")
    search_fields = ("number", "content")
    ordering = ("number",)


@admin.register(Memo)
class MemoAdmin(DocumentAdminMixin):
    list_display = (
        "number",
        "self_date",
        "type",
        "content",
        "get_topics",
        "get_addressees",
        "author",
    )
    filter_horizontal = ("addressee", "topic")
    list_filter = (
        "addressee",
        "author",
        "topic",
        "type",
        ("self_date", DateRangeFilter),
    )
    date_hierarchy = "self_date"
    inlines = [AttachedFileInline]
    search_fields = ("number", "content")
    fields = ("number", "self_date", "type", "content",
              "topic", "addressee", "author")

    def get_addressees(self, obj):
        return ", ".join([org.name for org in obj.addressee.all()])

    get_addressees.short_description = "Адресаты"


@admin.register(Act)
class ActAdmin(DocumentAdminMixin):
    list_display = ("number", "self_date", "content",
                    "stamp", "topic", "author")
    list_filter = (
        "stamp",
        "topic",
        "author",
        ("self_date", DateRangeFilter),
    )
    date_hierarchy = "self_date"
    inlines = [AttachedFileInline]
    fields = ("number", "self_date", "type", "content", "topic", "author")
    search_fields = ("number", "content")


@admin.register(OutgoingLetter)
class OutgoingLetterAdmin(DocumentAdminMixin):
    list_display = (
        "number",
        "self_date",
        "outgoing_date",
        "get_topics",
        "content",
        "get_addressees",
        "author",
        "get_disks",
        "incoming_letters_list",
    )
    filter_horizontal = ("addressee", "disk", "answers_to", "topic")
    list_filter = (
        "addressee",
        "topic",
        # Добавить сюда выпор письма для связи
        "author",
        ("outgoing_date", DateRangeFilter),
        ("self_date", DateRangeFilter),
    )
    date_hierarchy = "outgoing_date"
    inlines = [AttachedFileInline]
    fields = (
        "number",
        "self_date",
        "outgoing_date",
        "topic",
        "content",
        "addressee",
        "answers_to",
        "disk",
    )
    readonly_fields = ("incoming_letters_list",)
    search_fields = ("number", "content")

    def incoming_letters_list(self, obj):
        incoming_letters = obj.incoming_letters.all()
        if not incoming_letters:
            return "Нет ответов"
        return mark_safe(
            "<br>".join(
                f"<a href='/doc/incomingletter/?number={i.number}' class='minimal-link'>"
                f"<span class='icon'>📄</span>{i}</a>"
                for i in incoming_letters
            )
        )

    incoming_letters_list.short_description = "вх. ответы:"

    def get_addressees(self, obj):
        return ", ".join([org.name for org in obj.addressee.all()])

    get_addressees.short_description = "Адресаты"

    def get_disks(self, obj):
        return ", ".join([disk.number for disk in obj.disk.all()])

    get_disks.short_description = "Диски"

    def changelist_view(self, request, extra_context=None):
        # Контекст для кнопки
        if extra_context is None:
            extra_context = {}

        # Построим URL фильтрации по текущему пользователю
        filter_url = f"{reverse('admin:doc_outgoingletter_changelist')}?author__id__exact={request.user.id}"

        extra_context['my_letters_filter_url'] = filter_url

        return super().changelist_view(request, extra_context=extra_context)

    class Media:
        css = {
            'all': ('admin/css/linkstyle.css',)
        }


@admin.register(IncomingLetter)
class IncomingLetterAdmin(DocumentAdminMixin):
    list_display = (
        "number",
        "self_date",
        "sender_number",
        "info",
        "sender_date",
        "get_topics",
        "content",
        "addressee",
        "get_workers",
        "author",
        "answer_by_list",
    )
    list_filter = (
        "addressee",
        "topic",
        ("sender_date", DateRangeFilter),
        ("self_date", DateRangeFilter),
        "author",
        "workers",
    )
    filter_horizontal = ("workers", "answer_by", "topic")
    date_hierarchy = "sender_date"
    inlines = [AttachedFileInline]
    fields = (
        "number",
        "self_date",
        "sender_number",
        "info",
        "sender_date",
        "topic",
        "content",
        "addressee",
        "answer_by",
        "workers",
    )
    search_fields = (
        "number",
        "sender_number",
        "content",
        "info",
    )

    readonly_fields = ("answer_by_list",)

    def answer_by_list(self, obj):
        answer_by = obj.answer_by.all()
        answered_by_outgoing = obj.answered_by_outgoing.all()

        if not answer_by and not answered_by_outgoing:
            return "Нет ответов"

        links = []

        # Письма, на которые это входящее отвечает
        for i in answer_by:
            links.append(
                f"<a href='/doc/outgoingletter/?number={i.number}' class='minimal-link'>"
                f"<span class='icon'>📄</span>{i}</a>"
            )

    # Исходящие письма, которые ответили на это входящее
        for i in answered_by_outgoing:
            links.append(
                f"<a href='/doc/outgoingletter/?number={i.number}' class='minimal-link'>"
                f"<span class='icon'>📄</span>{i}</a>"
            )

        return mark_safe("<br>".join(links))

    answer_by_list.short_description = "ответ на исх:"

    def get_workers(self, obj):
        return ", ".join([worker.username for worker in obj.workers.all()])

    get_workers.short_description = "Исполнители"

    def changelist_view(self, request, extra_context=None):
        # Контекст для кнопки
        if extra_context is None:
            extra_context = {}

        # Построим URL фильтрации по текущему пользователю
        filter_url = f"{reverse('admin:doc_incomingletter_changelist')}?workers__id__exact={request.user.id}"

        extra_context['my_letters_filter_url'] = filter_url

        return super().changelist_view(request, extra_context=extra_context)

    class Media:
        css = {
            'all': ('admin/css/linkstyle.css',)
        }
