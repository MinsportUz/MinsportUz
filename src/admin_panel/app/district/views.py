from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView
from rolepermissions.mixins import HasRoleMixin

from admin_panel.model.territorial import District, Region
from . import forms
from admin_panel.app import views as custom


class DistrictCreate(HasRoleMixin, custom.CustomCreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = District
    form_class = forms.DistrictForm
    template_name = 'back/territorial/district/district_create.html'
    success_url = reverse_lazy('district:district-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DistrictCreate, self).get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        if data.get('region'):
            data['region'] = Region.objects.get(id=int(data['region']))
        print(data)
        obj = self.model.objects.create(**data)
        
        obj.save()
        return HttpResponseRedirect(self.success_url)
    

class DistrictList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = District
    template_name = 'back/territorial/district/district_list.html'
    queryset = model.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DistrictList, self).get_context_data(object_list=object_list)
        objects = self.queryset
    
        q = self.request.GET.get('q')
        if q:
            if self.request.LANGUAGE_CODE == 'en':
                objects = self.model.objects.filter(title_en__icontains=q)
            if self.request.LANGUAGE_CODE == 'ru':
                objects = self.model.objects.filter(title_ru__icontains=q)
            if self.request.LANGUAGE_CODE == 'uz':
                objects = self.model.objects.filter(title_uz__icontains=q)

        page = self.request.GET.get('page', 1)
        paginator = Paginator(objects, 12)

        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)

        context['objects'] = objects
        return context
    

class DistrictUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = District
    form_class = forms.DistrictForm
    context_object_name = 'district'
    template_name = 'back/territorial/district/district_update.html'
    success_url = reverse_lazy('district:district-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DistrictUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        if data.get('region'):
            data['region'] = Region.objects.get(id=int(data['region']))

        obj = self.model.objects.get(id=self.kwargs['pk'])

        obj.region = data.get('region')
        obj.title_uz = data.get('title_uz')
        obj.title_ru = data.get('title_ru')
        obj.title_en = data.get('title_en')

        obj.save()

        return HttpResponseRedirect(self.success_url)


class DistrictDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = District
    success_url = reverse_lazy('district:district-list')



