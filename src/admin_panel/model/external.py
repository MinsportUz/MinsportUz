from django.conf import settings
from django.db import models
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _

STATUS = (
    (0, _('news')),
    (1, _('event')),
)


class ExternalImage(models.Model):
    image = models.ImageField(upload_to='external')
    url = models.URLField()
    # type = models.IntegerField(choices=STATUS, default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'external_image'
        ordering = ['-id']

    def __str__(self):
        return str(self.url)

    @property
    def image_url(self):
        # "Returns the image url."
        if self.image:
            return '%s%s' % (settings.HOST, self.image.url)
        return ''
