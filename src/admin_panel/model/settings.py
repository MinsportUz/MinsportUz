from django.conf import settings
from django.db import models
# from sorl.thumbnail import ImageField

from admin_panel.common import generate_field


class MainPageSetting(models.Model):
    # logo_uz = models.FileField(upload_to='agency_logo')
    # logo_ru = models.FileField(upload_to='agency_logo')
    # logo_en = models.FileField(upload_to='agency_logo')

    logo_title = models.CharField(max_length=255)
    e_link = models.URLField(blank=True)
    phone_number = models.CharField(max_length=128, blank=True, null=True)
    menu_icon = models.FileField(upload_to='icon')
    menu_icon_link = models.CharField(max_length=255, null=True)

    mobile_title = models.CharField(max_length=255)
    mobile_description = models.TextField()
    mobile_image = models.FileField(upload_to='settings')
    mobile_poster = models.FileField(upload_to='settings')
    mobile_android = models.URLField()
    mobile_ios = models.URLField()

    home_ad = models.FileField(upload_to='settings')
    home_ad_android = models.URLField()
    home_ad_ios = models.URLField()
    poster = models.FileField(upload_to='poster')
    poster_url = models.URLField()

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'main_page_settings'

    def __str__(self):
        return 'main_page_settings'

    @property
    def icon_url(self):
        # Return icon url
        if self.menu_icon:
            return '%s%s' % (settings.HOST, self.menu_icon.url)

    @property
    def mobile_image_url(self):
        if self.mobile_image:
            return '%s%s' % (settings.HOST, self.mobile_image.url)

    @property
    def mobile_poster_url(self):
        if self.mobile_poster:
            return '%s%s' % (settings.HOST, self.mobile_poster.url)

    @property
    def poster_link(self):
        if self.poster:
            return '%s%s' % (settings.HOST, self.poster.url)

    @property
    def home_ad_url(self):
        if self.home_ad:
            return '%s%s' % (settings.HOST, self.home_ad.url)

    def save(self, *args, **kwargs):
        if self.logo_title_uz:
            self.logo_title_sr = generate_field(self.logo_title_uz)
        if self.mobile_description_uz:
            self.mobile_description_sr = generate_field(self.mobile_description_uz)
        if self.mobile_title_uz:
            self.mobile_title_sr = generate_field(self.mobile_title_uz)

        super(MainPageSetting, self).save(*args, **kwargs)


class ContactSetting(models.Model):
    address = models.TextField()
    buses = models.CharField(max_length=255, null=True, blank=True)
    mini_buses = models.CharField(max_length=255, null=True, blank=True)
    bus_station = models.CharField(max_length=255, null=True, blank=True)
    metro_station = models.CharField(max_length=255, null=True, blank=True)
    working_days = models.TextField()
    working_hours = models.TextField()
    email = models.EmailField()

    event_username = models.CharField(max_length=200, null=True, blank=True)
    news_username = models.CharField(max_length=200, null=True, blank=True)
    event_link = models.URLField(null=True, blank=True)
    news_link = models.URLField(null=True, blank=True)

    youtube = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    telegram = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    phone_number = models.CharField(max_length=50)

    notice = models.TextField(null=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contact_settings'

    def __str__(self):
        return 'contact_settings'

    def save(self, *args, **kwargs):
        if self.address_uz:
            self.address_sr = generate_field(self.address_uz)
        if self.bus_station_uz:
            self.bus_station_sr = generate_field(self.bus_station_uz)
        if self.metro_station_uz:
            self.metro_station_sr = generate_field(self.metro_station_uz)
        if self.working_days_uz:
            self.working_days_sr = generate_field(self.working_days_uz)

        if self.notice_uz:
            self.notice_sr = generate_field(self.notice_uz)

        super(ContactSetting, self).save(*args, **kwargs)


class Typo(models.Model):
    title = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    corrected = models.BooleanField(default=False)
    page = models.CharField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'typos'
        ordering = ['corrected', '-created_at']

    def __str__(self):
        return "{} {} {}".format(("Completed" if self.corrected else "Not completed"), self.created_at, self.page)
