from django.utils import timezone
from rest_framework import viewsets
from . import serializers
from admin_panel.model import tender
from api import pagination
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import activate


class CustomModalViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')

        return queryset


class TenderListView(CustomModalViewSet):
    queryset = tender.Tender.objects.filter(is_published=True).order_by(
        '-date')
    serializer_class = serializers.TenderSerializer
    pagination_class = None
    http_method_names = ['get']


class AdmTenderTypeView(viewsets.ModelViewSet):
    queryset = tender.Type.objects.all()
    serializer_class = serializers.AdmTypeSerializer
    pagination_class = None
    http_method_names = ['get']


class AdmTenderView(viewsets.ModelViewSet):
    queryset = tender.Tender.objects.all().order_by('-date')
    serializer_class = serializers.AdmTenderSerializer
    pagination_class = pagination.CustomPagination
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')

        return queryset


class AdmTenderTypeView(viewsets.ModelViewSet):
    queryset = tender.Type.objects.all()
    serializer_class = serializers.AdmTypeSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated, ]


class AdmTenderNoticesView(viewsets.ModelViewSet):
    queryset = tender.TenderNotices.objects.all().order_by('-id')
    serializer_class = serializers.AdmTenderNoticesSerializer
    pagination_class = pagination.CustomPagination
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        # lang = self.request.query_params.get('lang', 'uz')
        # activate(lang)
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')

        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.updated_at = timezone.now()
        tender.TenderNoticesPhotos.objects.filter(tender=instance.id).delete()
        instance.save()
        return super().update(request, *args, **kwargs)


class TenderNoticesView(viewsets.ModelViewSet):
    queryset = tender.TenderNotices.objects.filter(is_published=True).order_by('-id')
    serializer_class = serializers.TenderNoticesSerializer
    pagination_class = pagination.CustomPagination
    http_method_names = ['get', ]

    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')

        return queryset


class AdmTenderNoticesPhotosView(viewsets.ModelViewSet):
    queryset = tender.TenderNoticesPhotos.objects.all().order_by('-id')
    serializer_class = serializers.AdmTenderNoticesPhotosSerializer
    pagination_class = None
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')

        return queryset
