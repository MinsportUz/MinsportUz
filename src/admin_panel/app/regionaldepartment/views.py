from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView
from rolepermissions.mixins import HasRoleMixin

from admin_panel.model.territorial import RegionalDepartment
from . import forms
from admin_panel.app import views as custom



# Regional Department
class RegionalDepartmentCreate(HasRoleMixin, custom.CustomCreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = RegionalDepartment
    form_class = forms.RegionalDepartmentForm
    template_name = 'back/territorial/regionaldepartment/region_create.html'
    success_url = reverse_lazy('regionaldepartment:regionaldepartment-list')


class RegionalDepartmentList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = RegionalDepartment
    template_name = 'back/territorial/regionaldepartment/region_list.html'
    queryset = model.objects.all()


class RegionalDepartmentUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = RegionalDepartment
    form_class = forms.RegionalDepartmentForm
    context_object_name = 'object'
    template_name = 'back/territorial/regionaldepartment/region_update.html'
    success_url = reverse_lazy('regionaldepartment:regionaldepartment-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        region = RegionalDepartment.objects.get(id=self.kwargs['pk'])

        region.title_uz = data.get('title_uz')
        region.title_ru = data.get('title_ru')
        region.title_en = data.get('title_en')
        # region.phone_number = data.get('phone_number')

        region.save()

        return HttpResponseRedirect(self.success_url)


class RegionalDepartmentDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = RegionalDepartment
    success_url = reverse_lazy('regionaldepartment:regionaldepartment-list')