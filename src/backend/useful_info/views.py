from django.conf import settings
from rest_framework import generics, serializers

from useful_info.models import UsefulMaterial


class UsefulMaterialSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = UsefulMaterial
        fields = ("title", "url")

    def get_url(self, obj):
        if obj.file:
            return f"{settings.SITE_URL}{obj.file.url}"
        elif obj.link:
            return obj.link
        return None


class UsefulMaterialListAPIView(generics.ListAPIView):
    queryset = UsefulMaterial.objects.all()
    serializer_class = UsefulMaterialSerializer
