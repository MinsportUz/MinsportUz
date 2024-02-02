from rest_framework import serializers
from admin_panel.model import menu

class MenuDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = menu.Menu
        fields = [
            'id', 'title',
        ]


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = menu.Menu
        fields = [
            'id', 'parent', 'title_uz', 'title_ru', 'title_en', 'order', 'url', 'footer', 'is_static'
        ]


class MenuListSerializer(serializers.ModelSerializer):
    child = serializers.SerializerMethodField()
    class Meta:
        model = menu.Menu
        fields = [
            'id', 'title_uz', 'title_ru', 'title_en', 'order', 'url', 'child', 'footer', 'is_static'
        ]

    def get_child(self, obj):
        queryset = self.Meta.model.objects.filter(parent__isnull=False, parent=obj)
        if queryset.exists():
            return MenuSerializer(queryset, many=True).data
        return []

