from rest_framework import serializers
from admin_panel.model import menu, static
from django.conf import settings
from django.db.models import Count, Avg


class AdmMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = menu.Menu
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation[
            'parent_title_uz'] = (instance.parent.title_uz + ' -> ' + instance.title_uz) if instance.parent else instance.title_uz
        representation[
            'parent_title_ru'] = (instance.parent.title_ru + ' -> ' + instance.title_ru) if instance.parent else instance.title_ru
        representation[
            'parent_title_en'] = (instance.parent.title_en + ' -> ' + instance.title_en) if instance.parent else instance.title_en
        return representation


class AdmStaticPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = static.StaticPage
        fields = '__all__'