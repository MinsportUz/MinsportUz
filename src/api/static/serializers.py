from rest_framework import serializers
from admin_panel.model import static
from admin_panel.model import menu
from api.settings import serializers as menu_serializer
from django.conf import settings


class StaticSerializer(serializers.ModelSerializer):
    title_uz = serializers.CharField()
    title_ru = serializers.CharField()
    title_en = serializers.CharField()

    content_uz = serializers.CharField()
    content_ru = serializers.CharField()
    content_en = serializers.CharField()

    class Meta:
        model = static.StaticPage
        fields = [
            'id', 'title', 'url', 'slug', 'views', 'active', 'content', 'title_uz',
            'title_ru', 'title_en', 'content_uz', 'content_ru', 'content_en'
        ]


class StaticMenuSerializer(menu_serializer.HeaderSubMenuSerializer):
    class Meta:
        model = menu.Menu
        fields = [
            'id', 'title', 'url', 'is_static'
        ]


class StaticDataSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()

    class Meta:
        model = static.StaticData
        fields = [
            'id', 'url', 'slug', 'views', 'active', 'title', 'content', 'image', 'file', 'icon', 'main_url',
            'published_at'
        ]

    # def to_representation(self, instance):
    #     try:
    #         data = super().to_representation(instance)
    #         data['title'] = instance.title
    #         data['content'] = instance.content
    #         return data
    #     except Exception:
    #         return super().to_representation(instance)

    def get_icon(self, obj):
        return settings.HOST + obj.icon.url if obj.icon else None

    def get_image(self, obj):
        return settings.HOST + obj.image.url if obj.image else None

    def get_file(self, obj):
        return settings.HOST + obj.file.url if obj.file else None


class AdmStaticDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = static.StaticData
        fields = '__all__'
