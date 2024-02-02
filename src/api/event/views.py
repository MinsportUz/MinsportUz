from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
from admin_panel.model import event
from admin_panel.model import settings
from . import serializers
from api import pagination
from api import filters as custom_filter


class CustomModalViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')
        return queryset


class EventListView(CustomModalViewSet):
    queryset = event.Event.objects.filter(is_published=True).order_by(
        '-event_date')
    serializer_class = serializers.EventSerializer
    pagination_class = pagination.ExtraShort
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['hashtag']
    search_fields = ['title_uz', 'title_ru', 'title_en', ]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.EventDetailSerializer
        return serializers.EventSerializer

    """
    Filter BY date. Query params must be given in /?event_date format
    """

    def get_queryset(self):
        given_date = self.request.query_params.get('event_date')
        queryset = self.queryset.exclude(title__exact='')
        if given_date is not None:
            queryset = self.queryset.filter(event_date__gte=given_date).order_by('-event_date').exclude(title__exact='')
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        url = reverse('event-api-detail', args=(instance.id,), request=request)
        serializer = self.get_serializer_class()
        related = self.get_queryset().filter(type=instance.type).exclude(id=instance.id)[:4]
        payload = {
            'event': serializer(instance).data,
            'url': url,
            'related': serializer(related, many=True).data,

        }

        return Response(payload)


class IndexEventListView(CustomModalViewSet):
    queryset = event.Event.objects.filter(is_published=True).order_by(
        '-event_date')
    serializer_class = serializers.IndexEventSerializer
    pagination_class = pagination.ExtraShort
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer_class()
        link = settings.ContactSetting.objects.last()
        payload = {
            'username': link.event_username,
            'link': link.event_link,
            'events': serializer(instance, many=True).data,
        }
        return Response(payload)


class AdmEventView(viewsets.ModelViewSet):
    queryset = event.Event.objects.all()
    serializer_class = serializers.AdmEventSerializer
    # pagination_class = pagination.Short
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]
