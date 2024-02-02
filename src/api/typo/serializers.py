from rest_framework import serializers
from admin_panel.model import settings


class TypoSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.Typo
        fields = [
            'title', 'comment', 'page',
        ]
