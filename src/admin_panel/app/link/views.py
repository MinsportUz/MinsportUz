from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView
from rolepermissions.mixins import HasRoleMixin

from admin_panel.model.useful_link import UsefulLink
from . import forms
from admin_panel.app import views as custom


class LinkCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = UsefulLink
    form_class = forms.LinkForm
    template_name = 'back/useful_link/useful_link_create.html'
    success_url = reverse_lazy('link:link-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        link = self.model(**data)

        icon = request.FILES.get('icon')
        if icon:
            link.icon = icon
        link.save()
        return HttpResponseRedirect(self.success_url)


class LinkUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = UsefulLink
    form_class = forms.LinkForm
    context_object_name = 'object'
    template_name = 'back/useful_link/useful_link_update.html'
    success_url = reverse_lazy('link:link-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        link = self.model.objects.get(id=self.kwargs['pk'])
        icon = request.FILES.get('icon')
        if icon:
            link.icon = icon
        link.url = data.get('url')
        link.title_uz = data.get('title_uz')
        link.title_ru = data.get('title_ru')
        link.title_en = data.get('title_en')

        link.description_uz = data.get('description_uz')
        link.description_ru = data.get('description_ru')
        link.description_en = data.get('description_en')

        link.save()
        return HttpResponseRedirect(self.success_url)


class LinkList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = UsefulLink
    template_name = 'back/useful_link/useful_link_list.html'
    queryset = model.objects.all()


class LinkDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = UsefulLink
    success_url = reverse_lazy('link:link-list')
