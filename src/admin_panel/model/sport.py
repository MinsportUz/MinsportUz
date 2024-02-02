from django.conf import settings
from django.db import models
# from sorl.thumbnail import ImageField

from admin_panel.common import generate_field
from admin_panel.model.territorial import Region
from django_resized import ResizedImageField

# Image cropping conf
AVATAR = [120, 120]
IMAGE = [300, 170]


class Stadion(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    address = models.TextField(blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    host_team = models.CharField(max_length=350, blank=True, null=True)
    established = models.CharField(max_length=350, blank=True)
    capacity = models.IntegerField(default=0, blank=True, null=True)
    image = ResizedImageField(size=IMAGE, upload_to='stadion', blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stadion'
        ordering = ['region', '-created_at']

    def __str__(self):
        return str(self.title)

    @property
    def image_url(self):
        # "Returns the image url."
        return '%s%s' % (settings.HOST, self.image.url) if self.image else ""

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.description_uz:
            self.description_sr = generate_field(self.description_uz)
        if self.address_uz:
            self.address_sr = generate_field(self.address_uz)
        if self.host_team_uz:
            self.host_team_sr = generate_field(self.host_team_uz)
        if self.established_uz:
            self.established_sr = generate_field(self.established_uz)

        super(Stadion, self).save(*args, **kwargs)


class SportType(models.Model):
    title = models.CharField(max_length=250)
    # description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sport_type'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(SportType, self).save(*args, **kwargs)


class Champion(models.Model):
    title = models.CharField(max_length=250, null=True)
    sport = models.ForeignKey(SportType, on_delete=models.CASCADE)
    competition = models.TextField()
    description = models.TextField()
    image = ResizedImageField(size=AVATAR, upload_to='champion')
    medal = models.CharField(max_length=500)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'champion'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.title)

    @property
    def image_url(self):
        # "Returns the image url."
        return '%s%s' % (settings.HOST, self.image.url) if self.image else ''

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.competition_uz:
            self.competition_sr = generate_field(self.competition_uz)
        if self.description_uz:
            self.description_sr = generate_field(self.description_uz)
        if self.medal_uz:
            self.medal_sr = generate_field(self.medal_uz)

        super(Champion, self).save(*args, **kwargs)
