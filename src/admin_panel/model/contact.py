from django.db import models
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _
import uuid

from admin_panel.common import generate_field
from admin_panel.model import ministry
from admin_panel.model import ministry

STATUS = (
    (0, _('in process')),
    (1, _('reviewed')),
    (2, _('rejected')),
)


def id_number_generator(klass):
    last_obj = klass.objects.all().order_by('id').last()
    if not last_obj or not last_obj.id_number:
        return '00000001'
    reserve_no = last_obj.id_number
    width = 8
    new_reserve_int = int(reserve_no) + 1
    formatted = (width - len(str(new_reserve_int))) * "0" + str(new_reserve_int)
    new_reserve_int = str(formatted)
    return new_reserve_int


class ContactType(models.Model):
    title = models.CharField(max_length=300, null=True)
    order = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contact_type'
        ordering = ['order']

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(ContactType, self).save(*args, **kwargs)


class Contact(models.Model):
    sender_name = models.CharField(max_length=200)
    key = models.CharField(max_length=100, unique=True, null=True, blank=True)
    id_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    message = models.TextField()
    type = models.CharField(max_length=200, null=True, blank=True)
    image = models.FileField(upload_to='contact', null=True, blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    staff = models.ForeignKey(ministry.Staff, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'contact'
        ordering = ['status']

    def __str__(self):
        return str(self.sender_name)

    def save(self, *args, **kwargs):
        key = self.key
        if not key:
            key = uuid.uuid4().hex[:6].upper()
        while Contact.objects.filter(key=key).exclude(pk=self.pk).exists():
            key = uuid.uuid4().hex[:6].upper()

        self.key = key
        if not self.id_number:
            self.id_number = id_number_generator(Contact)
        super(Contact, self).save(*args, **kwargs)


class Feedback(models.Model):
    sender_name = models.CharField(max_length=200)
    email = models.CharField(max_length=250, null=True, blank=True)
    topic = models.TextField()
    message = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'feedback'

    def __str__(self):
        return str(self.sender_name)


class WeekDay(models.Model):
    title = models.CharField(max_length=100)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'week_day'

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(WeekDay, self).save(*args, **kwargs)


class Reception(models.Model):
    staff = models.ForeignKey(ministry.Staff, on_delete=models.CASCADE)
    day = models.ForeignKey(WeekDay, on_delete=models.CASCADE)
    time = models.CharField(max_length=500)
    active = models.BooleanField(default=False)
    # content = models.TextField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reception'
        ordering = ['-id']

    def __str__(self):
        if self.staff:
            return str(self.staff.title)
        return str(self.day)


class ContactStat(models.Model):
    total = models.CharField(max_length=200, null=True)
    review = models.CharField(max_length=200, null=True)
    process = models.CharField(max_length=200, null=True)
    reject = models.CharField(max_length=200, null=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contact_stat'

    def __str__(self):
        return 'Contact Statistics'
