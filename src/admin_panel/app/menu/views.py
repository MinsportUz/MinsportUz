import json

from django.core.serializers import serialize
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse_lazy
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rolepermissions.mixins import HasRoleMixin
from django.utils.translation import gettext as _

from admin_panel.app import views as custom
from admin_panel.model.menu import Menu
from django.views.generic import CreateView
from . import forms, serializers


# API create & update
# class MenuCreateAPIView(generics.CreateAPIView):
class MenuCreateAPIView(HasRoleMixin, APIView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    queryset = Menu.objects.all()
    serializer_class = serializers.MenuSerializer
    success_url = reverse_lazy('menu:menu-list')

    def get(self, request, format=None):
        parent = Menu.objects.filter(parent__isnull=True)
        child = Menu.objects.filter(parent__isnull=False)
        serializer = serializers.MenuListSerializer(parent, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        # print(data, 321123213321)
        serializer = self.serializer_class

        return Response('success', status=201)


class MenuCreateAPI(HasRoleMixin, APIView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'

    def post(self, request, *args, **kwargs):
        data = request.data.get('payload')
        try:
            Menu.objects.all().delete()
            for parent in data:
                new_parent = Menu.objects.create(title_uz=parent['title_uz'], title_ru=parent['title_ru'],
                                                 title_en=parent['title_en'],
                                                 order=parent['order'],
                                                 footer=parent['footer'],
                                                 url=parent['url'])
                if parent.get('child'):
                    # print('creating child')
                    for child in parent['child']:
                        Menu.objects.create(title_uz=child['title_uz'], title_ru=child['title_ru'],
                                            title_en=child['title_en'],
                                            order=child['order'],
                                            is_static=child['is_static'],
                                            parent=new_parent, url=child['url'])

            return Response(_("Muvaffaqiyatli saqlandi"), status=201)
        except:
            return Response(_("Xatolik yuz berdi"), status=200)


class MenuDeleteAPI(HasRoleMixin, APIView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'

    def post(self, request, *args, **kwargs):
        data = self.request.data.get('id')
        obj = Menu.objects.filter(id=int(data))
        if obj.exists():
            obj.last().delete()
            return Response('Menu deleted')
        else:
            return Response('Menu not deleted')


class MenuCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Menu
    form_class = forms.MenuForm
    template_name = 'back/menu/menu_create.html'
    success_url = reverse_lazy('menu:menu-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MenuCreate, self).get_context_data(object_list=object_list)
        lang = self.request.LANGUAGE_CODE
        api_url = '/panel/menu/api/'
        host = self.request.build_absolute_uri('/')[:-1]
        api = "%s/%s%s" % (host, lang, api_url)
        post = "%s/%s%screate/" % (host, lang, api_url)
        delete = "%s/%s%sdelete/" % (host, lang, api_url)
        context['api'] = api
        context['post'] = post
        context['delete'] = delete
        context['host'] = 'https://minsport.uz/'
        return context

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)
