from base64 import b64encode

from rest_framework import serializers

from profiles.models import UserFromTelegram

from .models import Mailing


class MailingSerializer(serializers.ModelSerializer):
    """
    Сериализатор объекта 'Mailing'.
    """

    image = serializers.SerializerMethodField()

    class Meta:
        model = Mailing
        fields = ("id", "text", "send_date", "image", "is_sended")

    def get_image(self, obj):
        if obj.image:
            with open(obj.image.path, "rb") as image_file:
                encoded_string = b64encode(image_file.read()).decode("utf-8")
            return encoded_string
        return None


class UserMailSerializer(serializers.ModelSerializer):
    """
    Сериализатор объекта 'UserFromTelegram' для получения списка пользователей.
    """

    class Meta:
        model = UserFromTelegram
        fields = ("telegram_id",)
