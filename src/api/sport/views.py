from rest_framework import viewsets
from rest_framework.response import Response

from admin_panel.model import sport
from . import serializers
from api import pagination
from rest_framework.permissions import IsAuthenticated


class CustomModalViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')

        return queryset


class StadionListView(viewsets.ModelViewSet):
    queryset = sport.Stadion.objects.all()
    serializer_class = serializers.StadionSerializer
    pagination_class = pagination.MidShort
    http_method_names = ['get']


class ChampionView(viewsets.ModelViewSet):
    queryset = sport.Champion.objects.all()
    serializer_class = serializers.ChampionSerializer
    pagination_class = None
    http_method_names = ['get']


class ChampionListView(viewsets.ModelViewSet):
    queryset = sport.Champion.objects.all()
    serializer_class = serializers.ChampionSerializer
    pagination_class = pagination.MidShort
    http_method_names = ['get']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        related = self.get_queryset().exclude(id=instance.id)[:4]
        serializer = self.serializer_class
        payload = {
            'data': serializer(instance).data,
            'related': serializer(related, many=True).data
        }
        return Response(payload, status=200)


class AdmStadionView(viewsets.ModelViewSet):
    queryset = sport.Stadion.objects.all()
    serializer_class = serializers.AdmStadionSerializer
    pagination_class = pagination.MidShort
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]


class AdmSportTypeView(viewsets.ModelViewSet):
    queryset = sport.SportType.objects.all()
    serializer_class = serializers.AdmSportTypeSerializer
    pagination_class = pagination.MidShort
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]


class AdmChampionView(viewsets.ModelViewSet):
    queryset = sport.Champion.objects.all()
    serializer_class = serializers.AdmChampionSerializer
    pagination_class = pagination.MidShort
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]
