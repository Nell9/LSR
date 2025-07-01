from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User

LENGHT_LIMIT = 20

User = get_user_model()


class Type(models.Model):
    type = models.CharField(verbose_name="Статус отправки", max_length=255)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Тип документа"
        verbose_name_plural = "Типы документов"
        ordering = ["type"]


class Organizations(models.Model):
    name = models.TextField(verbose_name="Название организации")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
        ordering = ["name"]


class Okr(models.Model):
    name = models.TextField(verbose_name="Название ОКР")

    class Meta:
        verbose_name = "Окр"
        verbose_name_plural = "Окр"
        ordering = ["name"]

    def __str__(self):
        return self.name


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


class Peoples(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Автор записи", auto_created=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ["name"]


class Letters(models.Model):
    number = models.CharField(
        verbose_name="Номер письма",
        max_length=255,
        null=False,
        help_text="(обязательное)",
    )
    type = models.ForeignKey(
        Type,
        null=True,
        verbose_name="Тип документа",
        related_name="letter",
        on_delete=models.PROTECT,
        help_text="(обязательное)",
        default=0,
    )
    addressee = models.ManyToManyField(
        Organizations,
        blank=True,
        verbose_name="Адресаты",
        help_text="(обязательное)",
    )
    content = models.TextField(
        verbose_name="Содержание",
        null=False,
        help_text="(обязательное)",
    )
    okr = models.ForeignKey(
        Okr,
        verbose_name="ОКР",
        on_delete=models.PROTECT,
        help_text="(не обязательное)",
        default=None,
        null=True,
        blank=True,
    )
    send_date = models.DateField(
        verbose_name="Дата отправки",
        editable=True,
        null=False,
        help_text="(обязательное) Добавьте от какого числа письмо",
    )
    disk = models.ManyToManyField(
        Disk,
        verbose_name="Диск",
        help_text=(
            "(не обязательное) Добавьте новый диск для записи " "через LPBurn."
        ),
        blank=True,
    )
    author = models.CharField(
        max_length=64,
        verbose_name="Автор записи",
        null=True,
        default="0",
        editable=False,
        help_text="Создается автоматически"
    )
    workers = models.ManyToManyField(
        User,
        verbose_name="Исполнители",
        help_text="(не обязательное) Добавьте исполнителей письма",
        blank=True,
    )

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"
        ordering = ["send_date"]
        constraints = [
            models.UniqueConstraint(fields=['number', 'send_date'], name='unique_number_send_date')
        ]
