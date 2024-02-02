from django.conf import settings
from django.db import models
from django.utils.text import slugify
from admin_panel.model.press_service import generate_unique_slug

from admin_panel.common import generate_field


class Region(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=300, null=True)
    image = models.FileField(upload_to='region')
    phone_number = models.CharField(max_length=50, null=True)

    # long = models.FloatField(null=True, blank=True)
    # lat = models.FloatField(null=True, blank=True)
    # weather_status = models.CharField(max_length=255, null=True, blank=True)
    # icon = models.CharField(max_length=128, null=True, blank=True)
    class Meta:
        db_table = 'regions'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title_en) != self.slug:
                self.slug = generate_unique_slug(Region, self.title_en)
        else:  # create
            self.slug = generate_unique_slug(Region, self.title_en)
        super(Region, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)

    @property
    def image_url(self):
        # "Returns the image url."
        return '%s%s' % (settings.HOST, self.image.url)



class RegionalDepartment(models.Model):
    title = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50, null=True)

    # long = models.FloatField(null=True, blank=True)
    # lat = models.FloatField(null=True, blank=True)
    # weather_status = models.CharField(max_length=255, null=True, blank=True)
    # icon = models.CharField(max_length=128, null=True, blank=True)
    class Meta:
        db_table = 'regional_department'
        ordering = ['-id']

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(RegionalDepartment, self).save(*args, **kwargs)


class District(models.Model):
    title = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        db_table = 'districts'
        ordering = ['-id']

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(District, self).save(*args, **kwargs)
