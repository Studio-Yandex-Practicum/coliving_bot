import json
import os

from django.conf import settings
from django.core.management import BaseCommand

from profiles.models import Location


class Command(BaseCommand):
    """
    Создает экземпляры объектов 'Location' из json-файла.
    """

    def handle(self, *args, **options):
        print("Создаю объекты 'Location'")
        try:
            path = os.path.join(settings.BASE_DIR, "fixtures/", "locations.json")
            data = json.load(open(path, "r", encoding="utf8"))
            Location.objects.bulk_create(
                [Location(**field) for field in [data["fields"] for data in data]],
                ignore_conflicts=True,
            )
            print("Успешно завершено")
        except FileNotFoundError:
            print("Файл не найден")
