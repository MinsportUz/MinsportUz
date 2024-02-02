from datetime import date, datetime

from django.conf import settings
from django.db import models
from django.utils import timezone
# from django.utils.timezone import now
# from sorl.thumbnail import ImageField
from django_resized import ResizedImageField

from admin_panel.common import generate_field
from admin_panel.model.sport import SportType
from admin_panel.model.territorial import Region

# Image cropping conf
THUMBNAIL = [300, 170]
IMAGE = [1200, 675]


class Event(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    address = models.TextField()
    event_place = models.TextField()
    link = models.URLField(null=True)
    image = ResizedImageField(size=IMAGE, upload_to='event')
    event_date = models.DateTimeField(default=timezone.now)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, related_name='event')
    type = models.ForeignKey(SportType, on_delete=models.CASCADE, null=True, related_name='event')
    hashtag = models.ManyToManyField('NewsHashtag', related_name='event', blank=True)
    # pin = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'events'
        ordering = ['-event_date']

    def __str__(self):
        return str(self.title)

    @property
    def image_url(self):
        # "Returns the image url."
        return '%s%s' % (settings.HOST, self.image.url) if self.image else ''

    @property
    def expired(self):
        # "Return if event is expired"
        date = self.event_date.strftime("%d-%m-%Y")
        today = datetime.now().strftime("%d-%m-%Y")
        result = date > today
        return result

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)

        if self.description_uz:
            self.description_sr = generate_field(self.description_uz)

        if self.address_uz:
            self.address_sr = generate_field(self.address_uz)

        if self.event_place_uz:
            self.event_place_sr = generate_field(self.event_place_uz)

        super(Event, self).save(*args, **kwargs)
