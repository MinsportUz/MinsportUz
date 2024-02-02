from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils.translation import activate
from admin_panel.model import static
from admin_panel.model import menu
from . import serializers
from api import pagination
from rest_framework.permissions import IsAuthenticated


class CustomModalViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')

        return queryset


class StaticView(CustomModalViewSet):
    queryset = static.StaticPage.objects.filter(active=True)
    serializer_class = serializers.StaticSerializer
    pagination_class = None
    http_method_names = ['get']
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.views += 1
        instance.save()

        serializer = self.serializer_class
        menu_serializer = serializers.StaticMenuSerializer
        page_menu = menu.Menu.objects.filter(url=instance.slug)
        if page_menu.exists():
            page_menu = page_menu.last()
            parent_menu = page_menu.parent
            result = menu.Menu.objects.filter(parent=parent_menu)

            payload = {
                'title': parent_menu.title,
                'menu': menu_serializer(result, many=True).data,
                'page': serializer(instance).data,

            }

        else:
            parent_menu = menu.Menu.objects.filter(parent__isnull=True).order_by('order').first()
            result = menu.Menu.objects.filter(parent=parent_menu)
            payload = {
                'title': parent_menu.title,
                'menu': menu_serializer(result, many=True).data,
                'page': serializer(instance).data,
            }
        return Response(payload, status=status.HTTP_200_OK)


class StaticDataView(viewsets.ModelViewSet):
    queryset = static.StaticData.objects.filter(active=True)
    serializer_class = serializers.StaticDataSerializer
    pagination_class = None
    http_method_names = ['get']
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        data = static.StaticData.objects.filter(url=kwargs['slug'])
        activate(language)
        # instance = self.get_object()
        # instance.views += 1
        # instance.save()
        serializer = self.serializer_class
        menu_serializer = serializers.StaticMenuSerializer
        page_menu = menu.Menu.objects.filter(url=data.first().slug)
        if page_menu.exists():
            page_menu = page_menu.last()
            parent_menu = page_menu.parent
            result = menu.Menu.objects.filter(parent=parent_menu)
        else:
            if data.first().slug == 'elonlar':
                parent_menu = menu.Menu.objects.filter(url='activity/tenders').last()
            else:
                parent_menu = menu.Menu.objects.filter(parent__isnull=True).order_by('order').first()
            result = menu.Menu.objects.filter(parent=parent_menu.parent)  # id = parent_menu.parent_id
        _serializer = serializer(data, many=True, context={'language': language})
        payload = {
            'title': parent_menu.title if parent_menu else None,
            'menu': menu_serializer(result, many=True).data,
            'data': _serializer.data,
        }
        return Response(payload, status=status.HTTP_200_OK)


class AdmStaticDataView(viewsets.ModelViewSet):
    queryset = static.StaticData.objects.all()
    serializer_class = serializers.AdmStaticDataSerializers
    pagination_class = pagination.CustomPagination
    permission_classes = [IsAuthenticated, ]
