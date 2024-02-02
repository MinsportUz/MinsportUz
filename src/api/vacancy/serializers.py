from rest_framework import serializers
from admin_panel.model import ministry, vacancy


class VacancySerializer(serializers.ModelSerializer):
    title_uz = serializers.CharField()
    title_ru = serializers.CharField()
    title_en = serializers.CharField()

    about_uz = serializers.CharField()
    about_ru = serializers.CharField()
    about_en = serializers.CharField()

    tasks_uz = serializers.CharField()
    tasks_ru = serializers.CharField()
    tasks_en = serializers.CharField()

    class Meta:
        model = vacancy.Vacancy
        fields = "__all__"


class EducationSerializer(serializers.ModelSerializer):
    title_uz = serializers.CharField()
    title_ru = serializers.CharField()
    title_en = serializers.CharField()

    class Meta:
        model = vacancy.Education
        fields = "__all__"


class EmploymentSerializer(serializers.ModelSerializer):
    title_uz = serializers.CharField()
    title_ru = serializers.CharField()
    title_en = serializers.CharField()

    class Meta:
        model = vacancy.Employment
        fields = "__all__"