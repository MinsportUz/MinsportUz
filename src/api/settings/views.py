from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models.functions import Lower
from admin_panel.model.territorial import RegionalDepartment
from django_filters.rest_framework import DjangoFilterBackend
from . import serializers
from admin_panel.model import settings, territorial
from admin_panel.model import menu
from admin_panel.model import useful_link
from api.views import DistrictSerializer, RegionDepartmentSerializer
from api import pagination
from rest_framework.permissions import IsAuthenticated


class CustomModalViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')

        return queryset


class SiteContactView(CustomModalViewSet):
    queryset = settings.ContactSetting.objects.all()
    serializer_class = serializers.SiteContactSerializer
    pagination_class = None
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset().last()
        serializer = self.get_serializer(instance).data
        return Response(serializer)


class HeaderView(CustomModalViewSet):
    queryset = settings.MainPageSetting.objects.all()
    serializer_class = serializers.HeaderSerializer
    pagination_class = None
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset().last()
        obj = menu.Menu.objects.filter(parent__isnull=True)
        serializer = self.serializer_class
        object_serializer = serializers.MenuSerializer
        regions = RegionalDepartment.objects.all()
        payload = {
            'site': serializer(instance).data,
            'region': RegionDepartmentSerializer(regions, many=True).data,
            'menu': object_serializer(obj, many=True).data}
        return Response(payload)


class FooterView(CustomModalViewSet):
    queryset = settings.ContactSetting.objects.all()
    serializer_class = serializers.FooterSerializer
    pagination_class = None
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset().last()
        obj = menu.Menu.objects.filter(parent__isnull=True, footer=True)
        serializer = self.get_serializer_class()
        object_serializer = serializers.MenuSerializer
        payload = {
            'footer': serializer(instance).data,
            'menu': object_serializer(obj, many=True).data,
        }
        return Response(payload)


class UsefulLinkView(CustomModalViewSet):
    queryset = useful_link.UsefulLink.objects.all()
    serializer_class = serializers.UsefulLinkSerializer
    pagination_class = None
    http_method_names = ['get']


class PosterView(CustomModalViewSet):
    queryset = settings.MainPageSetting.objects.all()
    serializer_class = serializers.PosterSerializer
    pagination_class = None
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset().last()
        serializer = self.get_serializer_class()
        return Response(serializer(instance).data)


class RegionView(CustomModalViewSet):
    queryset = territorial.Region.objects.all().order_by(Lower('title'))
    serializer_class = serializers.RegionSerializer
    pagination_class = None
    http_method_names = ['get', ]


class DistrictView(CustomModalViewSet):
    queryset = territorial.District.objects.all().order_by(Lower('title'))
    serializer_class = DistrictSerializer
    pagination_class = None
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['region', 'region__title']


class RegionDepartmentView(CustomModalViewSet):
    queryset = territorial.RegionalDepartment.objects.all()
    serializer_class = serializers.RegionDepartmentSerializer
    pagination_class = None
    http_method_names = ['get']


class HeaderDevView(viewsets.ModelViewSet):
    queryset = settings.MainPageSetting.objects.all()
    serializer_class = serializers.HeaderSerializer
    pagination_class = None


class MenuDevView(viewsets.ModelViewSet):
    queryset = menu.Menu.objects.all()
    serializer_class = serializers.MenuDevSerializer
    pagination_class = None


class AdmUsefulLinkView(viewsets.ModelViewSet):
    queryset = useful_link.UsefulLink.objects.all()
    serializer_class = serializers.AdmUsefulLinkSerializer
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')
        return queryset


class AdmMainPageSettingView(viewsets.ModelViewSet):
    queryset = settings.MainPageSetting.objects.all()
    serializer_class = serializers.AdmMainPageSettingSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]


class AdmContactSettingView(viewsets.ModelViewSet):
    queryset = settings.ContactSetting.objects.all()
    serializer_class = serializers.AdmContactSettingSerializer
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]


class AdmTypoView(viewsets.ModelViewSet):
    queryset = settings.Typo.objects.all()
    serializer_class = serializers.AdmTypoSerializer
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]


class AdmRegionView(viewsets.ModelViewSet):
    queryset = territorial.Region.objects.all()
    serializer_class = serializers.AdmRegionSerializer
    permission_classes = [IsAuthenticated, ]


class AdmDistrictView(viewsets.ModelViewSet):
    queryset = territorial.District.objects.all().order_by(Lower('title'))
    serializer_class = serializers.AdmDistrictSerializer
    # pagination_class = pagination.CustomPagination
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['region', 'region__title']


class AdmRegionDepartmentView(viewsets.ModelViewSet):
    queryset = territorial.RegionalDepartment.objects.all()
    serializer_class = serializers.AdmRegionDepartmentSerializer
    pagination_class = pagination.CustomPagination
    permission_classes = [IsAuthenticated, ]
