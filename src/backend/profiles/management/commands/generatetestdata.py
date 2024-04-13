import random

from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.core.management import BaseCommand
from PIL import Image

from images.models import ColivingImage, ProfileImage
from profiles.constants import ColivingTypes, Restrictions, Sex
from profiles.models import Coliving, Location, Profile, UserFromTelegram

TELEGRAM_ID_START = 1000000
COLIVING_ABOUT_CHOICES = [
    "IT-пространство с коворкингом и общей зоной",
    "Уютный дом для маркетологов и креативных профессионалов",
    "Студенческий коллектив с акцентом на образование и творчество",
    "Эко-жилье для любителей здорового образа жизни и спорта",
    "Проживание для геймеров с игровой комнатой и LAN-вечеринками",
    "Индустриальный коллаборатив с мастерскими и совместными проектами",
    "Уединенное место для художников с ателье и выставками",
    "Место сосредоточения стартапов с инкубатором и менторством",
    "Дом для литературных клубов и книжных вечеров",
    "Жилье для путешественников с культурными мероприятиями и экскурсиями",
]
PROFILE_ABOUT_CHOICES = [
    "Путешественник исследователь",
    "Любитель книг и кофе",
    "Фанат спорта и здорового образа жизни",
    "Художник-авангардист",
    "Инди-разработчик и мечтатель",
    "Студент искусств и музыки",
    "Лидер команды и предприниматель",
    "Фрилансер и фотограф",
    "Энтузиаст науки и технологий",
    "Любитель экстрима и приключений",
]


class Command(BaseCommand):
    help = "Заполняет БД тестовыми данными"

    def handle(self, *args, **options):
        if not Location.objects.exists():
            raise RuntimeError(
                "Нужно создать объекты Location"
                " или импортировать их с помощью команды import_locations."
            )

        num_users = 100
        for number in range(num_users):
            user = self._create_user(number)
            self._create_profile(number, user)
        for number in range(num_users // 2):
            self._create_coliving(number)
        for number in range(num_users // 2, num_users):
            self._set_user_residence(number)

    def _set_user_residence(self, number: int):
        user = UserFromTelegram.objects.get(telegram_id=TELEGRAM_ID_START + number)
        user.residence = random.choice(Coliving.objects.all())
        user.save()

    def _create_coliving(self, number: int):
        host = UserFromTelegram.objects.get(telegram_id=TELEGRAM_ID_START + number)
        location = random.choice(Location.objects.all())
        price = random.randint(Restrictions.PRICE_MIN, Restrictions.PRICE_MAX)
        room_type = random.choice(ColivingTypes.values)
        about = random.choice(COLIVING_ABOUT_CHOICES)
        coliving = Coliving.objects.create(
            host=host, location=location, price=price, room_type=room_type, about=about
        )
        self._create_coliving_image(coliving)

    def _create_coliving_image(self, coliving: Coliving):
        self._create_image(coliving, ColivingImage)

    def _create_profile(self, number: int, user: UserFromTelegram):
        name = f"User_{number}"
        sex = random.choice(Sex.values)
        age = random.randint(Restrictions.AGE_MIN, Restrictions.AGE_MAX)
        location = random.choice(Location.objects.all())
        about = random.choice(PROFILE_ABOUT_CHOICES)
        profile = Profile.objects.create(
            user=user, name=name, sex=sex, age=age, location=location, about=about
        )
        self._create_profile_image(profile)

    def _create_profile_image(self, profile: Profile):
        self._create_image(profile, ProfileImage)

    def _create_image(self, instance, image_model):
        white_image = Image.new("RGB", (1, 1), "white")
        temp_file = NamedTemporaryFile(suffix=".png")
        white_image.save(temp_file, format="PNG")
        temp_file.seek(0)
        django_file = ContentFile(temp_file.read())
        class_name = instance.__class__.__name__.lower()
        image_model.objects.create(
            **{class_name: instance},
            image=django_file,
            file_id=(
                "AgACAgIAAxkBAAI4b2YWSwABooTTLwrmxG1eyhTLC"
                "jQ4ewACbdYxGxussUjFdGMFQtfg-AEAAwIAA3kAAzQE"
            )
            if class_name == "profile"
            else (
                "AgACAgIAAxkBAAI4bmYWSwABE6wxkf3Yey8kY7Fzq"
                "ur_ewACo9cxGxussUgz-yVGNSObAwEAAwIAA3kAAzQE"
            ),
        )
        temp_file.close()

    def _create_user(self, number: int):
        telegram_id = TELEGRAM_ID_START + number
        user = UserFromTelegram.objects.create(telegram_id=telegram_id)
        return user
