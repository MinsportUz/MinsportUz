from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView
from rolepermissions.mixins import HasRoleMixin

from . import forms
from admin_panel.model.event import Event
from admin_panel.model.sport import SportType
from admin_panel.model import press_service as news
from admin_panel.model.territorial import Region
from admin_panel.app import views as custom


class EventCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Event
    form_class = forms.EventForm
    template_name = 'back/event/event_create.html'
    success_url = reverse_lazy('event:event-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EventCreate, self).get_context_data(object_list=object_list)
        context['types'] = SportType.objects.all()
        context['news_hashtags'] = news.NewsHashtag.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        hashtags = request.POST.getlist('hashtag')

        if data.get('hashtag'):
            del data['hashtag']

        if not data['event_date']:
            del data['event_date']

        if data.get('is_published') == 'on':
            data['is_published'] = True
        else:
            data['is_published'] = False

        data['region'] = Region.objects.get(id=int(data['region']))
        data['type'] = SportType.objects.get(id=int(data['type']))

        event = self.model.objects.create(**data)

        image = request.FILES.get('image')
        if image:
            event.image = image

        if request.LANGUAGE_CODE == 'en':
            for hashtag in hashtags:
                if news.NewsHashtag.objects.filter(title_en=hashtag).exists():
                    tag = news.NewsHashtag.objects.get(title_en=hashtag)
                    print('get')
                else:
                    tag = news.NewsHashtag.objects.create(title_en=hashtag)
                    print('create')

                print(event)

                event.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == 'ru':
            for hashtag in hashtags:
                if news.NewsHashtag.objects.filter(title_ru=hashtag).exists():
                    tag = news.NewsHashtag.objects.get(title_ru=hashtag)
                else:
                    tag = news.NewsHashtag.objects.create(title_ru=hashtag)

                event.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == 'uz':
            for hashtag in hashtags:
                if news.NewsHashtag.objects.filter(title_uz=hashtag).exists():
                    tag = news.NewsHashtag.objects.get(title_uz=hashtag)
                else:
                    tag = news.NewsHashtag.objects.create(title_uz=hashtag)

                event.hashtag.add(tag.id)

        event.save()

        return HttpResponseRedirect(self.success_url)


class EventList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Event
    template_name = 'back/event/event_list.html'
    queryset = model.objects.all()


class EventUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Event
    form_class = forms.EventForm
    context_object_name = 'event'
    template_name = 'back/event/event_update.html'
    success_url = reverse_lazy('event:event-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EventUpdate, self).get_context_data(object_list=object_list)
        context['types'] = SportType.objects.all()
        context['news_hashtags'] = news.NewsHashtag.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        hashtags = request.POST.getlist('hashtag')
        if data.get('hashtag'):
            del data['hashtag']

        event = Event.objects.get(id=self.kwargs['pk'])

        if not data['event_date']:
            del data['event_date']

        if data.get('is_published') == 'on':
            data['is_published'] = True
        else:
            data['is_published'] = False

        data['region'] = Region.objects.get(id=int(data['region']))
        data['type'] = SportType.objects.get(id=int(data['type']))

        event.title_uz = data.get('title_uz')
        event.title_ru = data.get('title_ru')
        event.title_en = data.get('title_en')

        event.description_uz = data.get('description_uz')
        event.description_ru = data.get('description_ru')
        event.description_en = data.get('description_en')

        event.address_uz = data.get('address_uz')
        event.address_ru = data.get('address_ru')
        event.address_en = data.get('address_en')

        event.event_place_uz = data.get('event_place_uz')
        event.event_place_ru = data.get('event_place_ru')
        event.event_place_en = data.get('event_place_en')

        event.link = data.get('link')

        if not data['event_date']:
            event.event_date = timezone.now()
        event.event_date = data.get('event_date')

        image = request.FILES.get('image')
        if image:
            event.image = image

        # Removing hashtags
        for i in event.hashtag.all():
            event.hashtag.remove(i)

        if request.LANGUAGE_CODE == 'en':
            for hashtag in hashtags:
                if news.NewsHashtag.objects.filter(title_en=hashtag).exists():
                    tag = news.NewsHashtag.objects.get(title_en=hashtag)
                else:
                    tag = news.NewsHashtag.objects.create(title_en=hashtag)
                if tag not in event.hashtag.all():
                    event.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == 'ru':
            for hashtag in hashtags:
                if news.NewsHashtag.objects.filter(title_ru=hashtag).exists():
                    tag = news.NewsHashtag.objects.get(title_ru=hashtag)
                else:
                    tag = news.NewsHashtag.objects.create(title_ru=hashtag)
                if tag not in event.hashtag.all():
                    event.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == 'uz':
            for hashtag in hashtags:
                if news.NewsHashtag.objects.filter(title_uz=hashtag).exists():
                    tag = news.NewsHashtag.objects.get(title_uz=hashtag)
                else:
                    tag = news.NewsHashtag.objects.create(title_uz=hashtag)
                if event not in event.hashtag.all():
                    event.hashtag.add(tag.id)

        event.save()

        return HttpResponseRedirect(self.success_url)


class EventDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Event
    success_url = reverse_lazy('event:event-list')
