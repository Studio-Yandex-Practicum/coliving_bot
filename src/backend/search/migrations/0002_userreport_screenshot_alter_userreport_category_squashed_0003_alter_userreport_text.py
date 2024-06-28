# Generated by Django 5.0.6 on 2024-06-28 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [
        ("search", "0002_userreport_screenshot_alter_userreport_category"),
        ("search", "0003_alter_userreport_text"),
    ]

    dependencies = [
        ("search", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userreport",
            name="screenshot",
            field=models.ImageField(null=True, upload_to="user_reports/"),
        ),
        migrations.AlterField(
            model_name="userreport",
            name="category",
            field=models.TextField(
                choices=[
                    ("Спам", "Спам"),
                    ("Не совпадают личные данные", "Не совпадают личные данные"),
                    ("Мошенник", "Мошенник"),
                    ("Запрещенная деятельность", "Запрещенная деятельность"),
                    ("Оскорбления, мат", "Оскорбления, мат"),
                    ("Другое", "Другое"),
                ],
                verbose_name="Категория",
            ),
        ),
        migrations.AlterField(
            model_name="userreport",
            name="text",
            field=models.TextField(blank=True, null=True, verbose_name="Текст"),
        ),
    ]
