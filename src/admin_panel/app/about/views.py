from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView
from rolepermissions.mixins import HasRoleMixin

from admin_panel.app.about import forms
from admin_panel.model.territorial import District, Region
from admin_panel.app.views import CustomCreateView, CustomUpdateView, CustomDeleteView, CustomListView
from admin_panel.model.ministry import AboutMinistry, MinistryStructure, MinistryStat, Department, Organization, Staff


class AboutMinistryUpdate(HasRoleMixin, View):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    success_url = reverse_lazy('about:about-update')

    def get(self, request):
        ministry = AboutMinistry.objects.last()
        return render(request, 'back/about/about_ministry.html', {'ministry': ministry})

    def post(self, request):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        ministry = AboutMinistry.objects.first()

        ministry.content_uz = data.get('content_uz')
        ministry.content_ru = data.get('content_ru')
        ministry.content_en = data.get('content_en')

        image = request.FILES.get('image')
        if image:
            ministry.image = image
        ministry.save()
        return HttpResponseRedirect(self.success_url)


class MininstryStructureUpdate(HasRoleMixin, View):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = MinistryStructure
    success_url = reverse_lazy('about:structure-update')

    def get(self, request):
        structure = self.model.objects.first()
        return render(request, 'back/about/structure_update.html', {'structure': structure})

    def post(self, request):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        structure = self.model.objects.first()

        structure.title_uz = data['title_uz']
        structure.title_ru = data['title_ru']
        structure.title_en = data['title_en']

        structure.content_uz = data['content_uz']
        structure.content_ru = data['content_ru']
        structure.content_en = data['content_en']

        structure.save()
        return HttpResponseRedirect(self.success_url)


class MinistryStatCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = MinistryStat
    form_class = forms.MinistryStatForm
    template_name = 'back/about/stat_create.html'
    success_url = reverse_lazy('about:stat-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        stat = self.model(**data)
        # stat.save()
        icon = request.FILES.get('icon')
        if icon:
            stat.icon = icon

        stat.save()
        return HttpResponseRedirect(self.success_url)


class MinistryStatUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = MinistryStat
    form_class = forms.MinistryStatForm
    success_url = reverse_lazy('about:stat-list')
    template_name = 'back/about/stat_update.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MinistryStatUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context['stat'] = self.model.objects.get(id=self.kwargs['pk'])

        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        stat = self.model.objects.get(id=self.kwargs['pk'])
        stat.title_uz = data['title_uz']
        stat.title_ru = data['title_ru']
        stat.title_en = data['title_en']
        stat.count = data['count']
        stat.colour = data['colour']

        icon = request.FILES.get('icon')
        if icon:
            stat.icon = icon

        stat.save()
        return HttpResponseRedirect(self.success_url)


class MinistryStatList(HasRoleMixin, CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = MinistryStat
    template_name = 'back/about/stat_list.html'
    queryset = model.objects.all()


class MinistryStatDelete(CustomDeleteView):
    model = MinistryStat
    success_url = reverse_lazy('about:stat-list')


# Department VIEWS
class DepartmentCreate(HasRoleMixin, CustomCreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Department
    form_class = forms.DepartmentForm
    template_name = 'back/department/department_create.html'
    success_url = reverse_lazy('about:department-list')


class DepartmentUpdate(CustomUpdateView):
    model = Department
    form_class = forms.DepartmentForm
    context_object_name = 'department'
    template_name = 'back/department/department_update.html'
    success_url = reverse_lazy('about:department-list')


class DepartmentList(HasRoleMixin, CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Department
    template_name = 'back/department/department_list.html'
    queryset = model.objects.all()


class DepartmentDelete(HasRoleMixin, CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Department
    success_url = reverse_lazy('about:department-list')


# Organization VIEWS
class OrganizationCreate(HasRoleMixin, CustomCreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Organization
    form_class = forms.OrganizationForm
    template_name = 'back/organization/organization_create.html'
    success_url = reverse_lazy('about:organization-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrganizationCreate, self).get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        context['districts'] = District.objects.all()

        return context


class OrganizationUpdate(HasRoleMixin, CustomUpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Organization
    form_class = forms.OrganizationForm
    context_object_name = 'organization'
    template_name = 'back/organization/organization_update.html'
    success_url = reverse_lazy('about:organization-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrganizationUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context['regions'] = Region.objects.all()
        context['districts'] = District.objects.all()

        return context


class OrganizationList(HasRoleMixin, CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Organization
    template_name = 'back/organization/organization_list.html'
    queryset = model.objects.all()


class OrganizationDelete(HasRoleMixin, CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Organization
    success_url = reverse_lazy('about:organization-list')


# Staff Views

class LeaderCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Staff
    form_class = forms.StaffForm
    template_name = 'back/staff/staff_create.html'
    success_url = reverse_lazy('about:staff-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LeaderCreate, self).get_context_data(object_list=object_list, **kwargs)
        context['departments'] = Department.objects.all()
        context['organizations'] = Organization.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        if data.get('main') == 'on':
            data['main'] = True
        else:
            data['main'] = False

        if data.get('leader') == 'on':
            data['leader'] = True
        else:
            data['leader'] = False

        if data.get('is_central') == 'on':
            data['is_central'] = True
        else:
            data['is_central'] = False
        # if not data.get('department', '') == '' and not data.get('department', 'None') == 'None':
        #     data['department'] = Department.objects.get(id=int(data['department']))
        #
        # elif data.get('department', 'None') == 'None':
        #     data['department'] = None
        # else:
        #     del data['department']

        # if not data.get('organization') == '' and not data.get('organization') == 'None':
        #     data['organization'] = Organization.objects.get(id=int(data['organization']))
        #
        # elif data.get('organization') == 'None':
        #     data['organization'] = None
        # else:
        #     del data['organization']

        staff = self.model.objects.create(**data)

        image = request.FILES.get('image')
        if image:
            staff.image = image

        staff.save()

        return HttpResponseRedirect(self.success_url)


class LeaderDepartmentCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Staff
    form_class = forms.StaffForm
    template_name = 'back/staff/staff_department_create.html'
    success_url = reverse_lazy('about:staff-department-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LeaderDepartmentCreate, self).get_context_data(object_list=object_list, **kwargs)
        context['departments'] = Department.objects.all()
        context['organizations'] = Organization.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        if data.get('main') == 'on':
            data['main'] = True
        else:
            data['main'] = False

        if data.get('leader') == 'on':
            data['leader'] = True
        else:
            data['leader'] = False

        if data.get('is_central') == 'on':
            data['is_central'] = True
        else:
            data['is_central'] = False
        # if not data.get('department') == '' and not data.get('department') == 'None':
        #     data['department'] = Department.objects.get(id=int(data['department']))
        #
        # elif data.get('department') == 'None':
        #     data['department'] = None
        # else:
        #     del data['department']

        # if not data.get('organization') == '' and not data.get('organization') == 'None':
        #     data['organization'] = Organization.objects.get(id=int(data['organization']))

        # elif data.get('organization') == 'None':
        #     data['organization'] = None
        # else:
        #     del data['organization']

        staff = self.model.objects.create(**data)

        image = request.FILES.get('image')
        if image:
            staff.image = image

        staff.save()

        return HttpResponseRedirect(self.success_url)


class LeaderOrganizationCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Staff
    form_class = forms.StaffForm
    template_name = 'back/staff/staff_organization_create.html'
    success_url = reverse_lazy('about:staff-organization-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LeaderOrganizationCreate, self).get_context_data(object_list=object_list, **kwargs)
        # context['departments'] = Department.objects.all()
        context['organizations'] = Organization.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        if data.get('main') == 'on':
            data['main'] = True
        else:
            data['main'] = False

        if data.get('leader') == 'on':
            data['leader'] = True
        else:
            data['leader'] = False

        if data.get('is_central') == 'on':
            data['is_central'] = True
        else:
            data['is_central'] = False

        # if not data.get('department') == '' and not data.get('department') == 'None':
        #     data['department'] = Department.objects.get(id=int(data['department']))

        # elif data.get('department') == 'None':
        #     data['department'] = None
        # else:
        #     del data['department']

        # if not data.get('organization') == '' and not data.get('organization') == 'None':
        #     data['organization'] = Organization.objects.get(id=int(data['organization']))
        #
        # elif data.get('organization') == 'None':
        #     data['organization'] = None
        # else:
        #     del data['organization']

        staff = self.model.objects.create(**data)

        image = request.FILES.get('image')
        if image:
            staff.image = image

        staff.save()

        return HttpResponseRedirect(self.success_url)


class LeaderCentralCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Staff
    form_class = forms.StaffForm
    template_name = 'back/staff/staff_central_create.html'
    success_url = reverse_lazy('about:staff-central-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LeaderCentralCreate, self).get_context_data(object_list=object_list, **kwargs)
        context['departments'] = Department.objects.all()
        context['organizations'] = Organization.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        if data.get('main') == 'on':
            data['main'] = True
        else:
            data['main'] = False

        if data.get('leader') == 'on':
            data['leader'] = True
        else:
            data['leader'] = False

        if data.get('is_central') == 'on':
            data['is_central'] = True
        else:
            data['is_central'] = False

        # if not data.get('department') == '' and not data.get('department') == 'None':
        #     data['department'] = Department.objects.get(id=int(data['department']))
        #
        # elif data.get('department') == 'None':
        #     data['department'] = None
        # else:
        #     del data['department']

        # if not data.get('organization') == '' and not data.get('organization') == 'None':
        #     data['organization'] = Organization.objects.get(id=int(data['organization']))
        #
        # elif data.get('organization') == 'None':
        #     data['organization'] = None
        # else:
        #     del data['organization']

        staff = self.model.objects.create(**data)

        image = request.FILES.get('image')
        if image:
            staff.image = image

        staff.save()

        return HttpResponseRedirect(self.success_url)


class LeaderUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Staff
    form_class = forms.StaffForm
    template_name = 'back/staff/staff_update.html'
    context_object_name = 'staff'
    success_url = reverse_lazy('about:staff-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LeaderUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context['departments'] = Department.objects.all()
        context['organizations'] = Organization.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        staff = self.model.objects.get(id=self.kwargs['pk'])

        if data.get('main') == 'on':
            data['main'] = True
        else:
            data['main'] = False

        if data.get('leader') == 'on':
            data['leader'] = True
        else:
            data['leader'] = False

        if data.get('is_central') == 'on':
            data['is_central'] = True
        else:
            data['is_central'] = False

        # if not data.get('department') == '' and not data.get('department') == 'None':
        #     data['department'] = Department.objects.get(id=int(data['department']))
        # elif data.get('department') == 'None':
        #     data['department'] = None
        # else:
        #     del data['department']

        # if not data.get('organization') == '' and not data.get('organization') == 'None':
        #     data['organization'] = Organization.objects.get(id=int(data['organization']))
        # elif data.get('organization') == 'None':
        #     data['organization'] = None
        # else:
        #     del data['organization']

        staff.title_uz = data['title_uz']
        staff.title_ru = data['title_ru']
        staff.title_en = data['title_en']

        staff.position_uz = data.get('position_uz')
        staff.position_ru = data.get('position_ru')
        staff.position_en = data.get('position_en')

        staff.organization = data.get('organization')
        staff.department = data.get('department')

        staff.work_history_uz = data.get('work_history_uz')
        staff.work_history_ru = data.get('work_history_ru')
        staff.work_history_en = data.get('work_history_en')

        staff.duty_uz = data.get('duty_uz')
        staff.duty_ru = data.get('duty_ru')
        staff.duty_en = data.get('duty_en')

        staff.reception_days_uz = data.get('reception_days_uz')
        staff.reception_days_ru = data.get('reception_days_ru')
        staff.reception_days_en = data.get('reception_days_en')
        staff.inner_phone_number = data.get('inner_phone_number')
        staff.email = data.get('email')

        staff.instagram = data.get('instagram')
        staff.telegram = data.get('telegram')
        staff.facebook = data.get('facebook')
        staff.twitter = data.get('twitter')

        staff.order = data.get('order')

        staff.main = data['main']
        staff.leader = data['leader']
        staff.is_central = data['is_central']

        image = request.FILES.get('image')
        if image:
            staff.image = image

        staff.save()

        return HttpResponseRedirect(self.success_url)


class LeaderDepartmentUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Staff
    form_class = forms.StaffForm
    template_name = 'back/staff/staff_deparment_update.html'
    context_object_name = 'staff'
    success_url = reverse_lazy('about:staff-department-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LeaderDepartmentUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context['departments'] = Department.objects.all()
        context['organizations'] = Organization.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        staff = self.model.objects.get(id=self.kwargs['pk'])

        if data.get('main') == 'on':
            data['main'] = True
        else:
            data['main'] = False

        if data.get('leader') == 'on':
            data['leader'] = True
        else:
            data['leader'] = False

        if data.get('is_central') == 'on':
            data['is_central'] = True
        else:
            data['is_central'] = False

        if not data.get('department') == '' and not data.get('department') == 'None':
            data['department'] = Department.objects.get(id=int(data['department']))
        elif data.get('department') == 'None':
            data['department'] = None
        else:
            del data['department']

        if not data.get('organization') == '' and not data.get('organization') == 'None':
            data['organization'] = Organization.objects.get(id=int(data['organization']))
        elif data.get('organization') == 'None':
            data['organization'] = None
        else:
            del data['organization']

        staff.title_uz = data['title_uz']
        staff.title_ru = data['title_ru']
        staff.title_en = data['title_en']

        staff.position_uz = data.get('position_uz')
        staff.position_ru = data.get('position_ru')
        staff.position_en = data.get('position_en')

        staff.organization = data.get('organization')
        staff.department = data.get('department')

        staff.work_history_uz = data.get('work_history_uz')
        staff.work_history_ru = data.get('work_history_ru')
        staff.work_history_en = data.get('work_history_en')

        staff.duty_uz = data.get('duty_uz')
        staff.duty_ru = data.get('duty_ru')
        staff.duty_en = data.get('duty_en')

        staff.reception_days_uz = data.get('reception_days_uz')
        staff.reception_days_ru = data.get('reception_days_ru')
        staff.reception_days_en = data.get('reception_days_en')
        staff.inner_phone_number = data.get('inner_phone_number')
        staff.email = data.get('email')

        staff.instagram = data.get('instagram')
        staff.telegram = data.get('telegram')
        staff.facebook = data.get('facebook')
        staff.twitter = data.get('twitter')

        staff.order = data.get('order')

        staff.main = data['main']
        staff.leader = data['leader']
        staff.is_central = data['is_central']

        image = request.FILES.get('image')
        if image:
            staff.image = image

        staff.save()

        return HttpResponseRedirect(self.success_url)


class LeaderOrganizationUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Staff
    form_class = forms.StaffForm
    template_name = 'back/staff/staff_organization_update.html'
    context_object_name = 'staff'
    success_url = reverse_lazy('about:staff-organization-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LeaderOrganizationUpdate, self).get_context_data(object_list=object_list, **kwargs)
        # context['departments'] = Department.objects.all()
        context['organizations'] = Organization.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        staff = self.model.objects.get(id=self.kwargs['pk'])

        if data.get('main') == 'on':
            data['main'] = True
        else:
            data['main'] = False

        if data.get('leader') == 'on':
            data['leader'] = True
        else:
            data['leader'] = False

        if data.get('is_central') == 'on':
            data['is_central'] = True
        else:
            data['is_central'] = False

        # if not data.get('department') == '' and not data.get('department') == 'None':
        #     data['department'] = Department.objects.get(id=int(data['department']))
        # elif data.get('department') == 'None':
        #     data['department'] = None
        # else:
        #     del data['department']

        if not data.get('organization') == '' and not data.get('organization') == 'None':
            data['organization'] = Organization.objects.get(id=int(data['organization']))
        elif data.get('organization') == 'None':
            data['organization'] = None
        else:
            del data['organization']

        staff.title_uz = data['title_uz']
        staff.title_ru = data['title_ru']
        staff.title_en = data['title_en']

        # staff.position_uz = data.get('position_uz')
        # staff.position_ru = data.get('position_ru')
        # staff.position_en = data.get('position_en')

        staff.organization = data.get('organization')
        # staff.department = data.get('department')

        # staff.work_history_uz = data.get('work_history_uz')
        # staff.work_history_ru = data.get('work_history_ru')
        # staff.work_history_en = data.get('work_history_en')

        # staff.duty_uz = data.get('duty_uz')
        # staff.duty_ru = data.get('duty_ru')
        # staff.duty_en = data.get('duty_en')

        # staff.reception_days_uz = data.get('reception_days_uz')
        # staff.reception_days_ru = data.get('reception_days_ru')
        # staff.reception_days_en = data.get('reception_days_en')
        # staff.inner_phone_number = data.get('inner_phone_number')
        # staff.email = data.get('email')

        # staff.instagram = data.get('instagram')
        # staff.telegram = data.get('telegram')
        # staff.facebook = data.get('facebook')
        # staff.twitter = data.get('twitter')

        # staff.order = data.get('order')

        staff.main = data['main']
        staff.leader = data['leader']
        staff.is_central = data['is_central']

        # image = request.FILES.get('image')
        # if image:
        #     staff.image = image

        staff.save()

        return HttpResponseRedirect(self.success_url)


class LeaderCentralUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Staff
    form_class = forms.StaffForm
    template_name = 'back/staff/staff_central_update.html'
    context_object_name = 'staff'
    success_url = reverse_lazy('about:staff-central-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LeaderCentralUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context['departments'] = Department.objects.all()
        context['organizations'] = Organization.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        staff = self.model.objects.get(id=self.kwargs['pk'])

        if data.get('main') == 'on':
            data['main'] = True
        else:
            data['main'] = False

        if data.get('leader') == 'on':
            data['leader'] = True
        else:
            data['leader'] = False

        if data.get('is_central') == 'on':
            data['is_central'] = True
        else:
            data['is_central'] = False

        # if not data.get('department') == '' and not data.get('department') == 'None':
        #     data['department'] = Department.objects.get(id=int(data['department']))
        # elif data.get('department') == 'None':
        #     data['department'] = None
        # else:
        #     del data['department']
        #
        # if not data.get('organization') == '' and not data.get('organization') == 'None':
        #     data['organization'] = Organization.objects.get(id=int(data['organization']))
        # elif data.get('organization') == 'None':
        #     data['organization'] = None
        # else:
        #     del data['organization']

        staff.title_uz = data['title_uz']
        staff.title_ru = data['title_ru']
        staff.title_en = data['title_en']

        staff.position_uz = data.get('position_uz')
        staff.position_ru = data.get('position_ru')
        staff.position_en = data.get('position_en')

        staff.organization = data.get('organization')
        staff.department = data.get('department')

        staff.work_history_uz = data.get('work_history_uz')
        staff.work_history_ru = data.get('work_history_ru')
        staff.work_history_en = data.get('work_history_en')

        staff.duty_uz = data.get('duty_uz')
        staff.duty_ru = data.get('duty_ru')
        staff.duty_en = data.get('duty_en')

        staff.reception_days_uz = data.get('reception_days_uz')
        staff.reception_days_ru = data.get('reception_days_ru')
        staff.reception_days_en = data.get('reception_days_en')
        staff.inner_phone_number = data.get('inner_phone_number')
        staff.email = data.get('email')

        staff.instagram = data.get('instagram')
        staff.telegram = data.get('telegram')
        staff.facebook = data.get('facebook')
        staff.twitter = data.get('twitter')

        staff.order = data.get('order')

        staff.main = data['main']
        staff.leader = data['leader']
        staff.is_central = data['is_central']

        image = request.FILES.get('image')
        if image:
            staff.image = image

        staff.save()

        return HttpResponseRedirect(self.success_url)


class LeaderList(HasRoleMixin, CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Staff
    template_name = 'back/staff/staff_list.html'
    queryset = model.objects.filter(is_central=False, department__isnull=True, organization__isnull=True)


class LeaderDepartmentList(HasRoleMixin, CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Staff
    template_name = 'back/staff/staff_department_list.html'
    queryset = model.objects.filter(main=False, leader=False, is_central=False, department__isnull=False)


class LeaderOrganizationList(HasRoleMixin, CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Staff
    template_name = 'back/staff/staff_organization_list.html'
    queryset = model.objects.filter(main=False, leader=False, is_central=False, organization__isnull=False)


class LeaderCentralList(HasRoleMixin, CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Staff
    template_name = 'back/staff/staff_central_list.html'
    queryset = model.objects.filter(leader=False, main=False, is_central=True)


# Must go to the current url
class LeaderDelete(HasRoleMixin, CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Staff
    success_url = reverse_lazy('about:staff-list')


# staff-department-list
class StaffDepartmentDelete(LeaderDelete):
    success_url = reverse_lazy('about:staff-department-list')


# staff-organization-list
class StaffOrganizationDelete(LeaderDelete):
    success_url = reverse_lazy('about:staff-organization-list')


# staff-central-list
class StaffCentralDelete(LeaderDelete):
    success_url = reverse_lazy('about:staff-central-list')
