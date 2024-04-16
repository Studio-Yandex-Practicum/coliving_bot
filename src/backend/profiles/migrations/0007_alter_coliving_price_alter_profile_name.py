# Generated by Django 5.0.1 on 2024-04-14 22:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0006_alter_location_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coliving",
            name="price",
            field=models.PositiveIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100000),
                ],
                verbose_name="Цена",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="name",
            field=models.TextField(
                validators=[
                    django.core.validators.MinLengthValidator(2),
                    django.core.validators.MaxLengthValidator(30),
                    django.core.validators.RegexValidator(
                        message="Числа и спец. символы не поддерживаются",
                        regex="^[А-Яа-яA-Za-z\\s'-]+$",
                    ),
                ],
                verbose_name="Имя пользователя",
            ),
        ),
    ]
