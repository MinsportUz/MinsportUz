from django.conf import settings
from django.db import models

from admin_panel.common import generate_field


class UsefulLink(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    icon = models.FileField(upload_to='icon')
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'useful_links'
        ordering = ['-id']

    def __str__(self):
        return str(self.title)

    @property
    def icon_url(self):
        # "Returns the image url."
        return '%s%s' % (settings.HOST, self.icon.url) if self.icon else ""

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.description_uz:
            self.description_sr = generate_field(self.description_uz)

        super(UsefulLink, self).save(*args, **kwargs)
