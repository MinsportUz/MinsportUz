from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView
from rolepermissions.mixins import HasRoleMixin

from . import forms
from admin_panel.app import views as custom
from ...model.static import StaticPage


class StaticCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = StaticPage
    form_class = forms.StaticForm
    template_name = 'back/static_page/static_page_create.html'
    success_url = reverse_lazy('static:static-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StaticCreate, self).get_context_data(object_list=object_list, **kwargs)
        host = self.request.build_absolute_uri('/')[:-1]
        context['site_url'] = host + '/' + 'static/'
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        if data.get('active') == 'on':
            data['active'] = True
        else:
            data['active'] = False

        obj = self.model(**data)
        obj.save()
        return HttpResponseRedirect(self.success_url)


class StaticUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = StaticPage
    form_class = forms.StaticForm
    context_object_name = 'object'
    template_name = 'back/static_page/static_page_update.html'
    success_url = reverse_lazy('static:static-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StaticUpdate, self).get_context_data(object_list=object_list, **kwargs)
        host = self.request.build_absolute_uri('/')[:-1]
        context['site_url'] = host + '/' + 'static/'
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        obj = self.model.objects.get(id=self.kwargs['pk'])

        if data.get('active') == 'on':
            data['active'] = True
        else:
            data['active'] = False

        obj.title_uz = data.get('title_uz')
        obj.title_ru = data.get('title_ru')
        obj.title_en = data.get('title_en')
        obj.content_uz = data.get('content_uz')
        obj.content_ru = data.get('content_ru')
        obj.content_en = data.get('content_en')
        obj.url = data.get('url')
        obj.active = data.get('active')

        obj.save()
        return HttpResponseRedirect(self.success_url)


class StaticList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = StaticPage
    template_name = 'back/static_page/static_page_list.html'
    queryset = model.objects.all()


class StaticDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = StaticPage
    success_url = reverse_lazy('static:static-list')
