# Generated by Django 5.0.6 on 2024-06-28 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userfromtelegram",
            name="is_banned",
            field=models.BooleanField(
                default=False,
                verbose_name="Заблокировать пользователя",
                null=False,
            ),
        ),
    ]
