# Generated by Django 5.2.3 on 2025-07-04 08:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doc", "0006_alter_act_self_date_alter_incomingletter_self_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="incomingletter",
            name="info",
            field=models.TextField(
                blank=True, null=True, verbose_name="Исполнитель + номер телефона"
            ),
        ),
        migrations.AlterField(
            model_name="act",
            name="self_date",
            field=models.DateField(
                default=datetime.datetime(
                    2025, 7, 4, 8, 10, 54, 545799, tzinfo=datetime.timezone.utc
                ),
                help_text="(обязательное) Дата письма в нашей организации",
                verbose_name="Дата письма",
            ),
        ),
        migrations.AlterField(
            model_name="incomingletter",
            name="self_date",
            field=models.DateField(
                default=datetime.datetime(
                    2025, 7, 4, 8, 10, 54, 545799, tzinfo=datetime.timezone.utc
                ),
                help_text="(обязательное) Дата письма в нашей организации",
                verbose_name="Дата письма",
            ),
        ),
        migrations.AlterField(
            model_name="incomingletter",
            name="sender_date",
            field=models.DateField(
                default=datetime.datetime(
                    2025, 7, 4, 8, 10, 54, 546799, tzinfo=datetime.timezone.utc
                ),
                help_text="(обязательное) Дата отправителя",
                verbose_name="Дата письма",
            ),
        ),
        migrations.AlterField(
            model_name="memo",
            name="self_date",
            field=models.DateField(
                blank=True,
                default=datetime.datetime(
                    2025, 7, 4, 8, 10, 54, 545799, tzinfo=datetime.timezone.utc
                ),
                help_text="(не обязательно) Дата СЗ в нашей организации можно заполнить позже",
                null=True,
                verbose_name="Дата СЗ",
            ),
        ),
        migrations.AlterField(
            model_name="outgoingletter",
            name="self_date",
            field=models.DateField(
                default=datetime.datetime(
                    2025, 7, 4, 8, 10, 54, 545799, tzinfo=datetime.timezone.utc
                ),
                help_text="(обязательное) Дата письма в нашей организации",
                verbose_name="Дата письма",
            ),
        ),
    ]
