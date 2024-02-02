from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from rolepermissions.mixins import HasRoleMixin

from admin_panel.app import views as custom
from . import forms
from ...model.vacancy import Vacancy, Employment, Education


class VacancyCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Vacancy
    form_class = forms.VacancyForm
    template_name = 'back/vacancy/vacancy_create.html'
    success_url = reverse_lazy('vacancy:vacancy-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacancyCreate, self).get_context_data(object_list=object_list)
        context['employments'] = Employment.objects.all()
        context['educations'] = Education.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        if data['education']:
            data['education'] = Education.objects.get(id=data['education'])

        if data['employment']:
            data['employment'] = Employment.objects.get(id=data['employment'])

        if data.get('is_published') == 'on':
            data['is_published'] = True
        else:
            data['is_published'] = False

        if not data['date']:
            del data['date']

        obj = self.model(**data)

        obj.save()
        return HttpResponseRedirect(self.success_url)


class VacancyUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Vacancy
    form_class = forms.VacancyForm
    template_name = 'back/vacancy/vacancy_update.html'
    context_object_name = 'object'
    success_url = reverse_lazy('vacancy:vacancy-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacancyUpdate, self).get_context_data(object_list=object_list)
        context['employments'] = Employment.objects.all()
        context['educations'] = Education.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        obj = self.model.objects.get(id=self.kwargs['pk'])

        if data['education']:
            data['education'] = Education.objects.get(id=data['education'])

        if data['employment']:
            data['employment'] = Employment.objects.get(id=data['employment'])

        if data.get('is_published') == 'on':
            data['is_published'] = True
        else:
            data['is_published'] = False

        if not data['date']:
            del data['date']

        obj.title_uz = data['title_uz']
        obj.title_ru = data['title_ru']
        obj.title_en = data['title_en']

        obj.about_uz = data['about_uz']
        obj.about_ru = data['about_ru']
        obj.about_en = data['about_en']

        obj.tasks_uz = data['tasks_uz']
        obj.tasks_ru = data['tasks_ru']
        obj.tasks_en = data['tasks_en']

        obj.employment = data['employment']
        obj.education = data['education']
        obj.is_published = data['is_published']
        obj.count = data['count']
        obj.date = data['date']

        obj.save()
        return HttpResponseRedirect(self.success_url)


class VacancyList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Vacancy
    template_name = 'back/vacancy/vacancy_list.html'
    queryset = model.objects.all()


class VacancyDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Vacancy
    success_url = reverse_lazy('vacancy:vacancy-list')
