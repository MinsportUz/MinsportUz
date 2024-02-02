from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import serializers
from api.news import serializers as news_serializers
from api import pagination

from admin_panel.model import press_service
from admin_panel.model import settings
from admin_panel.model import external


class CustomModalViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')

        return queryset


class PhotoListView(CustomModalViewSet):
    queryset = press_service.PhotoGallery.objects.filter(is_published=True).order_by(
        '-publish_date')
    serializer_class = serializers.PhotoSerializer
    pagination_class = pagination.MidShort
    http_method_names = ['get']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.PhotoDetailSerializer
        return serializers.PhotoSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        related = self.get_queryset().exclude(id=instance.id)[:4]
        related_serializer = serializers.PhotoSerializer
        instance.views += 1
        instance.save()

        payload = {
            'image': self.get_serializer(instance).data,
            'related': related_serializer(related, many=True).data
        }
        return Response(payload)


class IndexPhotoListView(CustomModalViewSet):
    queryset = external.ExternalImage.objects.all()
    serializer_class = serializers.ExternalImageSerializer
    pagination_class = None
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.serializer_class
        link = settings.ContactSetting.objects.last()

        payload = {
            'username': link.news_username if link else '',
            'link': link.news_link if link else '',
            'images': serializer(instance, many=True).data,
        }

        return Response(payload)


class VideoListView(CustomModalViewSet):
    queryset = press_service.VideoGallery.objects.filter(is_published=True).order_by(
        '-publish_date')
    serializer_class = serializers.VideoSerializer
    pagination_class = pagination.MidShort
    http_method_names = ['get']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        return Response(self.serializer_class(instance).data)


class AdmExternalImageView(viewsets.ModelViewSet):
    queryset = external.ExternalImage.objects.all()
    serializer_class = serializers.ExternalImageSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated,]
