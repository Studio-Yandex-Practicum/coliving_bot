from rest_framework.test import APITestCase

from profiles.models import Location, Profile, UserFromTelegram
from search.models import UserReport
from search.serializers import UserReportSerializer


class ReportSerializerTests(APITestCase):
    """Тесты для UserReportSerializer и MatchListSerializer."""

    @classmethod
    def setUpTestData(cls):
        cls.test_user_1 = UserFromTelegram.objects.create(telegram_id=1)
        cls.test_user_2 = UserFromTelegram.objects.create(telegram_id=2)
        cls.location = Location.objects.create(name="location")
        cls.user_profile = Profile.objects.create(
            user=cls.test_user_1, name="Vlad", age=25, location=cls.location
        )

        cls.report_data = {
            "reporter": cls.test_user_1.pk,
            "reported_user": cls.test_user_2.pk,
            "text": "test_text",
            "category": "Категория 1",
        }

        cls.invalid_report_data = {
            "reporter": "invalid_reporter",
            "reported_user": 99999,
            "text": "",
            "category": "invalid_category",
        }

        cls.serializer_data = {
            "telegram_id": cls.test_user_1.pk,
            "name": "Vlad",
            "age": 25,
        }

    def test_invalid_report_data(self):
        """Тест на сериализацию некорректных данных."""
        serializer = UserReportSerializer(data=self.invalid_report_data)
        self.assertFalse(serializer.is_valid())

    def test_missing_required_report_fields(self):
        """Тест на сериализацию пустых данных."""
        invalid_data = {}
        serializer = UserReportSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_valid_data_create_report(self):
        """Тест создания жалобы с валидными данными в сериализаторе."""
        serializer = UserReportSerializer(data=self.report_data)
        serializer.is_valid()
        serializer.save()
        created_report = UserReport.objects.get(reporter=self.test_user_1.pk)
        self.assertIsNotNone(created_report)
        self.assertEqual(created_report.reporter, self.test_user_1)
