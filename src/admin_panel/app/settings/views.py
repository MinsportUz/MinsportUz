from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView, ListView
from rolepermissions.mixins import HasRoleMixin

from admin_panel.model.settings import MainPageSetting, ContactSetting


class GeneralSettings(HasRoleMixin, View):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = MainPageSetting
    success_url = reverse_lazy('settings:general')

    def get(self, request):
        site = self.model.objects.first()

        return render(request, 'back/settings/main_page_settings.html', {'site': site})

    def post(self, request):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        site = self.model.objects.first()

        site.logo_title_uz = data.get('logo_title_uz')
        site.logo_title_ru = data.get('logo_title_ru')
        site.logo_title_en = data.get('logo_title_en')

        site.mobile_title_uz = data.get('mobile_title_uz')
        site.mobile_title_ru = data.get('mobile_title_ru')
        site.mobile_title_en = data.get('mobile_title_en')
        site.mobile_description_uz = data.get('mobile_description_uz')
        site.mobile_description_ru = data.get('mobile_description_ru')
        site.mobile_description_en = data.get('mobile_description_en')


        site.menu_icon_link = data.get('menu_icon_link')

        mobile_image = request.FILES.get('mobile_image')

        if mobile_image:
            site.mobile_image = mobile_image

        mobile_poster = request.FILES.get('mobile_poster')
        if mobile_poster:
            site.mobile_poster = mobile_poster

        home_ad = request.FILES.get('home_ad')
        if home_ad:
            site.home_ad = home_ad

        poster = request.FILES.get('poster')
        if poster:
            site.poster = poster

        menu_icon = request.FILES.get('menu_icon')
        if menu_icon:
            site.menu_icon = menu_icon

        # URL and non translatable charFields
        site.phone_number = data.get('phone_number')
        site.e_link = data.get('e_link')
        site.mobile_android = data.get('mobile_android')
        site.mobile_ios = data.get('mobile_ios')
        site.home_ad_android = data.get('home_ad_android')
        site.home_ad_ios = data.get('home_ad_ios')
        site.poster_url = data.get('poster_url')

        site.save()
        return HttpResponseRedirect(self.success_url)


class ContactSettings(HasRoleMixin, View):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    success_url = reverse_lazy('settings:contact')
    model = ContactSetting

    def get(self, request):
        contact = self.model.objects.first()
        return render(request, 'back/settings/contact_settings.html', {'contact': contact})

    def post(self, request):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        contact = self.model.objects.first()

        contact.address_uz = data.get('address_uz')
        contact.address_ru = data.get('address_ru')
        contact.address_en = data.get('address_en')

        contact.bus_station_uz = data.get('bus_station_uz')
        contact.bus_station_ru = data.get('bus_station_ru')
        contact.bus_station_en = data.get('bus_station_en')

        contact.notice_uz = data.get('notice_uz')
        contact.notice_ru = data.get('notice_ru')
        contact.notice_en = data.get('notice_en')

        contact.metro_station_uz = data.get('metro_station_uz')
        contact.metro_station_ru = data.get('metro_station_ru')
        contact.metro_station_en = data.get('metro_station_en')

        contact.working_days_uz = data.get('working_days_uz')
        contact.working_days_ru = data.get('working_days_ru')
        contact.working_days_en = data.get('working_days_en')

        contact.working_hours = data.get('working_hours')


        contact.phone_number = data.get('phone_number')
        contact.email = data.get('email')
        contact.mini_buses = data.get('mini_buses')
        contact.buses = data.get('buses')
        contact.event_link = data.get('event_link')
        contact.event_username = data.get('event_username')
        contact.news_link = data.get('news_link')
        contact.news_username = data.get('news_username')
        contact.instagram = data.get('instagram')
        contact.youtube = data.get('youtube')
        contact.telegram = data.get('telegram')
        contact.facebook = data.get('facebook')
        contact.twitter = data.get('twitter')

        contact.save()
        return HttpResponseRedirect(self.success_url)
