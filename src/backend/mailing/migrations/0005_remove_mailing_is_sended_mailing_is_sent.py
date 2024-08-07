# Generated by Django 5.0.6 on 2024-06-14 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0004_mailing_is_sended"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mailing",
            name="is_sended",
        ),
        migrations.AddField(
            model_name="mailing",
            name="is_sent",
            field=models.CharField(
                choices=[
                    ("is_waiting", "Ждёт"),
                    ("is_sending", "Отправляется"),
                    ("is_sent", "Отправлено"),
                ],
                default="is_waiting",
                max_length=20,
                verbose_name="Отправлено",
            ),
        ),
    ]
