from django.db.models import Count, Sum
from rest_framework import serializers
from collections import Counter

from admin_panel.model import question


class QuestionSerializer(serializers.RelatedField):
    def to_representation(self, obj):
        data = {
            'id': obj.id,
            'title': obj.title,
            'percentage': obj.percentage,
            # 'count': obj.count,
        }
        return data

    # def to_internal_value(self, id):
    #     return question.Quizz.objects.get(id=id)


class QuizzSerializer(serializers.ModelSerializer):
    class Meta:
        model = question.Quizz
        fields = [
            'id', 'title', 'result_count',
        ]


class QuizzDetailSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = question.Quizz
        fields = [
            'id', 'title', 'result_count', 'question',
        ]


class QuestionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = question.QuestionResult
        fields = ['question', 'quizz']


class AdmQuizzSerializer(serializers.ModelSerializer):
    class Meta:
        model = question.Quizz
        fields = '__all__'


class AdmQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = question.Question
        fields = '__all__'


class AdmQuestionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = question.QuestionResult
        fields = '__all__'