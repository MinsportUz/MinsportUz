from rest_framework import serializers
from admin_panel.model import settings


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.MainPageSetting
        fields = "__all__"
