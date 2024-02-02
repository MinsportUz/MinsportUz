from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from rolepermissions.mixins import HasRoleMixin

from admin_panel.app import views as custom
from admin_panel.model.tender import Tender, Type
from django.views.generic import CreateView, UpdateView
from . import forms
from ...model.territorial import Region


class TenderCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Tender
    form_class = forms.TenderForm
    template_name = 'back/tender/tender_create.html'
    success_url = reverse_lazy('tender:tender-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TenderCreate, self).get_context_data(object_list=object_list, **kwargs)
        context['types'] = Type.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        data['region'] = Region.objects.get(id=int(data['region']))
        data['type'] = Type.objects.get(id=int(data['type']))

        if data.get('is_published') == 'on':
            data['is_published'] = True
        else:
            data['is_published'] = False

        if not data['date']:
            del data['date']

        obj = self.model.objects.create(**data)

        file = request.FILES.get('file')
        if file:
            obj.file = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class TenderUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'

    model = Tender
    form_class = forms.TenderForm
    context_object_name = 'object'
    template_name = 'back/tender/tender_update.html'
    success_url = reverse_lazy('tender:tender-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TenderUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context['types'] = Type.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        data['region'] = Region.objects.get(id=int(data['region']))
        data['type'] = Type.objects.get(id=int(data['type']))

        if data.get('is_published') == 'on':
            data['is_published'] = True
        else:
            data['is_published'] = False

        if not data['date']:
            del data['date']

        obj = self.model.objects.get(id=self.kwargs['pk'])

        obj.title_uz = data.get('title_uz')
        obj.title_ru = data.get('title_ru')
        obj.title_en = data.get('title_en')

        obj.organizer_uz = data.get('organizer_uz')
        obj.organizer_ru = data.get('organizer_ru')
        obj.organizer_en = data.get('organizer_en')

        obj.number = data.get('number')
        obj.region = data.get('region')
        obj.type = data.get('type')
        obj.date = data.get('date')
        obj.is_published = data.get('is_published')

        file = request.FILES.get('file')
        if file:
            obj.file = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class TenderList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Tender
    template_name = 'back/tender/tender_list.html'
    queryset = model.objects.all()


class TenderDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Tender
    success_url = reverse_lazy('tender:tender-list')
