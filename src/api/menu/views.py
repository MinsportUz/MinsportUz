from django.utils.timezone import now
from rest_framework import viewsets, status, generics
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from admin_panel.model import ministry, menu, static
from . import serializers
from .. import pagination

from datetime import datetime, timedelta
from django.utils.timezone import make_aware


# class CustomModalViewSet(viewsets.ModelViewSet):
#     def get_queryset(self):
#         queryset = self.queryset
#         if hasattr(self.queryset.model, 'title'):
#             queryset = self.queryset.exclude(title__exact='')
#         return queryset
#
#
# class AboutUsView(CustomModalViewSet):
#     queryset = ministry.AboutMinistry.objects.all()
#     serializer_class = serializers.AboutUsSerializer
#     pagination_class = None
#     http_method_names = ['get']
#
#     def list(self, request):
#         stat = serializers.StatSerializer(ministry.MinistryStat.objects.all(), many=True).data
#         about = serializers.AboutUsSerializer(self.get_queryset(), many=True).data
#         dict = {
#             'about': about,
#             'stat': stat,
#         }
#         return Response(dict, status=status.HTTP_200_OK)


class AdmMenuView(viewsets.ModelViewSet):
    queryset = menu.Menu.objects.all()
    serializer_class = serializers.AdmMenuSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated, ]


class AdmStaticPageView(viewsets.ModelViewSet):
    queryset = static.StaticPage.objects.all()
    serializer_class = serializers.AdmStaticPageSerializer
    pagination_class = pagination.CustomPagination
    permission_classes = [IsAuthenticated, ]