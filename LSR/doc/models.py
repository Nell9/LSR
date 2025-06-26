
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models


LENGHT_LIMIT = 20

User = get_user_model()


class Type(models.Model):
    type = models.CharField(
        verbose_name='Статус отправки',
        max_length=255
    )


class Organizations(models.Model):
    name = models.TextField(
        verbose_name="Название организации"
    )


class Disk(models.Model):
    number = models.CharField(
        verbose_name='Номер диска',
        max_length=255,
        null=False
    )
    copyes = models.IntegerField(
        verbose_name="Количество копий",
        null=False
    )
    content = models.TextField(
        verbose_name='Содержание',
        null=False
    )


class Letter(models.Model):
    number = models.CharField(
        verbose_name='Номер письма',
        max_length=255
    )
    type = models.ForeignKey(
        Type,
        null=True,
        verbose_name='Тип документа',
        related_name='letters',
        on_delete=models.PROTECT,
        help_text='Акт, СЗ, Входящее...',
        default=0
    )
    addressee = models.ForeignKey(
        Organizations,
        null=True,
        on_delete=models.PROTECT,
        verbose_name='Адресаты'
    )
    content = models.TextField(
        verbose_name='Содержание',
        null=False
    )
    send_date = models.DateTimeField(
        verbose_name='Дата отправки',
        auto_now=True,
        null=False
    )
    disk = models.OneToOneField(
        Disk,
        verbose_name="Диск",
        on_delete=models.CASCADE,
        null=True,
        help_text="Добавьте диск для записи через LPBurn"
    )

    class Meta:
        verbose_name = ('Письмо')
        verbose_name_plural = ('Письма')
        ordering = ['send_date']
