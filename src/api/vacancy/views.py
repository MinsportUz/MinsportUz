from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from admin_panel.model import vacancy
from . import serializers


class AdmVacancyView(viewsets.ModelViewSet):
    queryset = vacancy.Vacancy.objects.all()
    serializer_class = serializers.VacancySerializer
    pagination_class = None
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]


class AdmEducationView(viewsets.ModelViewSet):
    queryset = vacancy.Education.objects.all()
    serializer_class = serializers.EducationSerializer
    pagination_class = None
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]


class AdmEmploymentView(viewsets.ModelViewSet):
    queryset = vacancy.Employment.objects.all()
    serializer_class = serializers.EmploymentSerializer
    pagination_class = None
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]
