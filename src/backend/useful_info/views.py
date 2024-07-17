from rest_framework import generics, serializers

from useful_info.models import UsefulMaterial


class UsefulMaterialSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = UsefulMaterial
        fields = ("title", "url")

    def get_url(self, obj):
        if obj.file:
            return self.context["request"].build_absolute_uri(obj.file.url)
        elif obj.link:
            return obj.link
        return None


class UsefulMaterialListAPIView(generics.ListAPIView):
    queryset = UsefulMaterial.objects.all()
    serializer_class = UsefulMaterialSerializer
