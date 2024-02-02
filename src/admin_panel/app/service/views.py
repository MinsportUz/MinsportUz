from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from rolepermissions.mixins import HasRoleMixin

from admin_panel.app import views as custom
from admin_panel.model.service import Service
from . import forms


class ServiceCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Service
    form_class = forms.ServiceForm
    template_name = 'back/service/service_create.html'
    success_url = reverse_lazy('service:service-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        service = self.model.objects.create(**data)

        icon = request.FILES.get('icon')
        if icon:
            service.icon = icon
        service.save()
        return HttpResponseRedirect(self.success_url)


class ServiceUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Service
    form_class = forms.ServiceForm
    template_name = 'back/service/service_update.html'
    context_object_name = 'service'
    success_url = reverse_lazy('service:service-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        service = self.model.objects.get(id=self.kwargs['pk'])

        icon = request.FILES.get('icon')
        if icon:
            service.icon = icon

        service.title_uz = data.get('title_uz')
        service.title_ru = data.get('title_ru')
        service.title_en = data.get('title_en')
        service.url = data.get('url')
        service.order = data.get('order')
        service.save()

        return HttpResponseRedirect(self.success_url)


class ServiceList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Service
    template_name = 'back/service/service_list.html'
    queryset = model.objects.all()
    success_url = reverse_lazy('service:service-list')


class ServiceDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Service
    success_url = reverse_lazy('service:service-list')
