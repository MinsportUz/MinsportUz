from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView
from rolepermissions.mixins import HasRoleMixin

from admin_panel.model.territorial import Region
from . import forms
from admin_panel.app import views as custom


class RegionCreate(HasRoleMixin, custom.CustomCreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Region
    form_class = forms.RegionForm
    template_name = 'back/territorial/region/region_create.html'
    success_url = reverse_lazy('region:region-list')


class RegionList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Region
    template_name = 'back/territorial/region/region_list.html'
    queryset = model.objects.all()


class RegionUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Region
    form_class = forms.RegionForm
    context_object_name = 'object'
    template_name = 'back/territorial/region/region_update.html'
    success_url = reverse_lazy('region:region-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        region = Region.objects.get(id=self.kwargs['pk'])

        region.title_uz = data.get('title_uz')
        region.title_ru = data.get('title_ru')
        region.title_en = data.get('title_en')
        # region.phone_number = data.get('phone_number')

        image = request.FILES.get('image')
        if image:
            region.image = image
        region.save()

        return HttpResponseRedirect(self.success_url)


class RegionDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Region
    success_url = reverse_lazy('region:region-list')



