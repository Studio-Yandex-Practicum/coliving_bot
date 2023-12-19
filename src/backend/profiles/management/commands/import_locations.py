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
            path = (
                os.path.join(settings.BASE_DIR, "fixtures/", "locations.json")
            )
            locations = json.load(open(path, "r", encoding="utf8"))
            for location in locations:
                Location.objects.create(**location['fields'])
            print("Успешно завершено")
        except FileNotFoundError:
            print("Файл не найден")
