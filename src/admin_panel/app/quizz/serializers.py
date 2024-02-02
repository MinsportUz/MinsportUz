from rest_framework import serializers
from admin_panel.model import question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = question.Question
        fields = [
            'id', 'title_uz', 'title_ru', 'title_en'
        ]
