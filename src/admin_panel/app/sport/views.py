from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from rolepermissions.mixins import HasRoleMixin

from admin_panel.app import views as custom
from admin_panel.model.sport import Champion, SportType, Stadion
from . import forms

# TYPE VIEWS
from ...model.territorial import Region


class TypeCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = SportType
    form_class = forms.TypeForm
    template_name = 'back/sport/sport_type_create.html'
    success_url = reverse_lazy('sport:type-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        type = self.model(**data)
        type.save()
        return HttpResponseRedirect(self.success_url)


class TypeUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = SportType
    form_class = forms.TypeForm
    template_name = 'back/sport/sport_type_update.html'
    context_object_name = 'type'
    success_url = reverse_lazy('sport:type-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        service = self.model.objects.get(id=self.kwargs['pk'])

        service.title_uz = data.get('title_uz')
        service.title_ru = data.get('title_ru')
        service.title_en = data.get('title_en')
        service.save()
        return HttpResponseRedirect(self.success_url)


class TypeList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = SportType
    template_name = 'back/sport/sport_type_list.html'
    queryset = model.objects.all()


class TypeDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = SportType
    success_url = reverse_lazy('sport:type-list')


# STADION
class StadionCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Stadion
    form_class = forms.StadionForm
    template_name = 'back/sport/stadion_create.html'
    success_url = reverse_lazy('sport:stadion-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        data['region'] = Region.objects.get(id=int(data['region']))

        stadion = self.model(**data)

        image = request.FILES.get('image')
        if image:
            stadion.image = image
        stadion.save()
        return HttpResponseRedirect(self.success_url)


class StadionUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Stadion
    form_class = forms.StadionForm
    template_name = 'back/sport/stadion_update.html'
    context_object_name = 'object'
    success_url = reverse_lazy('sport:stadion-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        stadion = self.model.objects.get(id=self.kwargs['pk'])

        image = request.FILES.get('image')
        if image:
            stadion.image = image

        stadion.title_uz = data.get('title_uz')
        stadion.title_ru = data.get('title_ru')
        stadion.title_en = data.get('title_en')

        stadion.description_uz = data.get('description_uz')
        stadion.description_ru = data.get('description_ru')
        stadion.description_en = data.get('description_en')

        stadion.address_uz = data.get('address_uz')
        stadion.address_ru = data.get('address_ru')
        stadion.address_en = data.get('address_en')

        stadion.host_team_uz = data.get('host_team_uz')
        stadion.host_team_ru = data.get('host_team_ru')
        stadion.host_team_en = data.get('host_team_en')

        stadion.established_uz = data.get('established_uz')
        stadion.established_ru = data.get('established_ru')
        stadion.established_en = data.get('established_en')

        stadion.capacity = data.get('capacity')

        stadion.save()
        return HttpResponseRedirect(self.success_url)


class StadionList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Stadion
    template_name = 'back/sport/stadion_list.html'
    queryset = model.objects.all()


class StadionDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Stadion
    success_url = reverse_lazy('sport:stadion-list')


# CHAMPION
class ChampionCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Champion
    form_class = forms.ChampionForm
    # template_name = 'back/sport/champion_create.html'
    template_name = 'back/sport/champion_create.html'
    success_url = reverse_lazy('sport:champion-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ChampionCreate, self).get_context_data(object_list=object_list, **kwargs)
        context['sport_types'] = SportType.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        data['sport'] = SportType.objects.get(id=int(data['sport']))

        obj = self.model(**data)

        image = request.FILES.get('image')
        if image:
            obj.image = image
        obj.save()
        return HttpResponseRedirect(self.success_url)


class ChampionUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Champion
    form_class = forms.ChampionForm
    template_name = 'back/sport/champion_update.html'
    context_object_name = 'object'
    success_url = reverse_lazy('sport:champion-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ChampionUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context['sport_types'] = SportType.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        obj = self.model.objects.get(id=self.kwargs['pk'])

        image = request.FILES.get('image')
        if image:
            obj.image = image

        data['sport'] = SportType.objects.get(id=int(data['sport']))

        obj.sport = data.get('sport')

        obj.title_uz = data.get('title_uz')
        obj.title_ru = data.get('title_ru')
        obj.title_en = data.get('title_en')

        obj.description_uz = data.get('description_uz')
        obj.description_ru = data.get('description_ru')
        obj.description_en = data.get('description_en')

        obj.competition_uz = data.get('competition_uz')
        obj.competition_ru = data.get('competition_ru')
        obj.competition_en = data.get('competition_en')

        obj.medal_uz = data.get('medal_uz')
        obj.medal_ru = data.get('medal_ru')
        obj.medal_en = data.get('medal_en')

        obj.save()
        return HttpResponseRedirect(self.success_url)


class ChampionList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Champion
    template_name = 'back/sport/champion_list.html'
    queryset = model.objects.all()


class ChampionDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Champion
    success_url = reverse_lazy('sport:champion-list')
