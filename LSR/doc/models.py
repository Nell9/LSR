from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from django.contrib.contenttypes.fields import GenericRelation
import os
from django.utils.text import slugify
LENGHT_LIMIT = 20

User = get_user_model()

# Модель для хранения тем документов
# Используется для Memo, Act, IncomingLetter и OutgoingLetter


class topics(models.Model):
    name = models.TextField(verbose_name="Тема документа")

    class Meta:
        verbose_name = "Темы документа"
        verbose_name_plural = "Темы документов"
        ordering = ["name"]

    def __str__(self):
        return self.name


def attachment_upload_path(instance, filename):
    """
    Формирует путь вида: attachments/<имя_модели>/имя_файла
    """
    if instance.content_object:
        model_name = instance.content_object.__class__.__name__.lower()
    else:
        model_name = 'unknown'

    folder = slugify(model_name)
    return os.path.join('attachments', folder, filename)


class AttachedFile(models.Model):
    file = models.FileField(
        upload_to=attachment_upload_path,
        verbose_name='Файл',
        help_text='Загрузите связанный файл',
        blank=True,
        null=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Generic relation:
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.file.name

# Модель для хранения организаций


class Organizations(models.Model):
    name = models.TextField(verbose_name="Название организации")
    addressee = models.TextField(
        verbose_name="Адрес организации",
        default="Не указано",
        help_text="(не обязательно) Адрес организации, "
                  "можно заполнить позже",
    )
    head = models.TextField(
        verbose_name="Руководитель организации",
        default="Не указано",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
        ordering = ["name"]


class Disk(models.Model):
    number = models.CharField(
        verbose_name="Номер диска", max_length=255, null=False)
    copyes = models.IntegerField(verbose_name="Количество копий", null=False)
    content = models.TextField(verbose_name="Содержание", null=False)

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = "Диск"
        verbose_name_plural = "Диски"
        ordering = ["number"]


class Document(models.Model):
    number = models.CharField(
        verbose_name="Номер письма",
        max_length=255,
        null=False,
        help_text="(обязательное) Номер письма в нашей организации",
    )
    self_date = models.DateField(
        verbose_name="Дата письма",
        editable=True,
        null=False,
        help_text="(обязательное) Дата письма в нашей организации",
        default=now(),
    )
    topic = models.ManyToManyField(
        topics,
        verbose_name="Тема документа",
    )
    content = models.TextField(
        verbose_name="Содержание",
        null=False,
        help_text="(обязательное)",
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор записи",
        help_text="Создается автоматически",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        auto_created=True,
        related_name="%(class)s_authors",
        editable=False,
    )

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = ""
        verbose_name_plural = "s"
        abstract = True
        ordering = ["self_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["number", "self_date"], name="unique_number_self_date"
            )
        ]


class Memo(Document):
    number = models.CharField(
        verbose_name="Номер СЗ",
        max_length=255,
        null=True,
        blank=True,
        help_text="(не обязательно) Номер СЗ в нашей организации можно заполнить позже",
    )
    type = models.CharField(
        verbose_name="Тип СЗ",
        max_length=255,
        help_text="(обязательное) Входящая/Исходящая",
        default="Не известно",
        null=False,
        choices=[
            ("Входящая", "Входящая"),
            ("Исходящая", "Исходящая"),
        ]
    )
    addressee = models.ManyToManyField(
        Organizations,
        blank=True,
        verbose_name="Адресаты",
        help_text="(обязательное)",
    )
    self_date = models.DateField(
        verbose_name="Дата СЗ",
        editable=True,
        null=True,
        blank=True,
        help_text=(
            "(не обязательно) Дата СЗ в нашей "
            "организации можно заполнить позже"
        ),
        default=now(),
    )
    attachments = GenericRelation(AttachedFile)

    class Meta:
        verbose_name = "Служебная записка"
        verbose_name_plural = "Служебные записки"


class Act(Document):
    type = models.CharField(
        verbose_name="Тип акта",
        max_length=255,
        null=False,
        help_text="(обязательное) Тип акта",
        default="О создании",
        choices=[
            ("О создании", "О создании"),
            ("Об уничтожении", "Об уничтожении"),
            ("О стирании", "О стирании"),
        ]
    )
    stamp = models.CharField(
        verbose_name="Гриф",
        max_length=255,
        null=False,
        default="Без грифа",
        choices=[
            ("Несекретно", "Несекретно"),
            ("ДСП", "ДСП"),
            ("Секретно", "Секретно"),
            ("Совершенно секретно", "Совершенно секретно"),
        ]
    )
    topic = models.CharField(
        verbose_name="Тема акта",
        max_length=255,
        null=False,
        help_text="(обязательное) Тема акта",
        default="Не указана",
    )
    attachments = GenericRelation(AttachedFile)

    class Meta:
        verbose_name = "Акт"
        verbose_name_plural = "Акты"


class OutgoingLetter(Document):
    outgoing_date = models.DateField(
        verbose_name="Дата отправки",
        editable=True,
        null=True,
        blank=True,
        help_text="(Не обязательно) Когда письмо было отправлено",
    )
    addressee = models.ManyToManyField(
        Organizations,
        blank=True,
        verbose_name="Адресаты",
        help_text="(обязательное)",
    )
    disk = models.ManyToManyField(
        Disk,
        verbose_name="Диск",
        help_text=(
            "(не обязательное) Добавьте новый диск для записи " "через LPBurn."),
        blank=True,
    )
    answers_to = models.ManyToManyField(
        'IncomingLetter',
        verbose_name='Ответ на вх. письмо',
        blank=True,
        related_name='answered_by_outgoing',
    )
    attachments = GenericRelation(AttachedFile)

    def __str__(self):
        return f"Исх. №{self.number} от {self.self_date}"

    class Meta:
        verbose_name = "Исходящее письмо"
        verbose_name_plural = "Исходящие письма"


class IncomingLetter(Document):
    sender_number = models.CharField(
        verbose_name="Номер письма отправителя",
    )
    sender_date = models.DateField(
        verbose_name="Дата письма",
        editable=True,
        null=False,
        help_text="(обязательное) Дата отправителя",
        default=now(),
    )
    addressee = models.ForeignKey(
        Organizations,
        null=True,
        verbose_name="Адресат",
        on_delete=models.PROTECT,
        help_text="(обязательное)",
    )

    workers = models.ManyToManyField(
        User,
        verbose_name="Исполнители",
        help_text="(не обязательное) Добавьте исполнителей письма",
        blank=True,
        related_name="assigned_letters",
    )
    answer_by = models.ManyToManyField(
        OutgoingLetter,
        verbose_name="Ответ на исх. письмо",
        null=True,
        blank=True,
        related_name="incoming_letters",
    )
    attachments = GenericRelation(AttachedFile)
    info = models.TextField(
        verbose_name="Информация об исполнителях",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Вх. №{self.number} от {self.self_date}"

    class Meta:
        verbose_name = "Входящее письмо"
        verbose_name_plural = "Входящие письма"
