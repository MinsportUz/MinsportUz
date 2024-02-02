from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from admin_panel.common import generate_field
from admin_panel.model import press_service


class DocType(models.Model):
    title = models.CharField(max_length=500, null=True)
    link = models.CharField(max_length=500, null=True)
    slug = models.SlugField(unique=True, max_length=500, null=True)
    # icon = models.FileField(upload_to='icon', null=True, blank=True)
    order = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'doctype'
        ordering = ['order', '-created_at']

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.link:  # edit
            if slugify(self.link) != self.slug:
                self.slug = press_service.generate_unique_slug(DocType, self.link)
        else:  # create
            self.slug = press_service.generate_unique_slug(DocType, self.link)
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)

        super(DocType, self).save(*args, **kwargs)


class Docs(models.Model):
    title = models.CharField(max_length=500)
    issued_by = models.CharField(max_length=500)
    file = models.FileField(upload_to='file', null=True, blank=True)
    law = models.CharField(max_length=500, blank=True, null=True)
    url = models.URLField(null=True)
    link = models.URLField(blank=True, null=True)
    doc_type = models.ForeignKey(DocType, on_delete=models.CASCADE, null=True, related_name='docs')
    date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'docs'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.issued_by_uz:
            self.issued_by_sr = generate_field(self.issued_by_uz)
        if self.law_uz:
            self.law_sr = generate_field(self.law_uz)
        super(Docs, self).save(*args, **kwargs)



    @property
    def file_url(self):
        # "Returns the image url."
        if self.file:
            return '%s%s' % (settings.HOST, self.file.url)
        return ''


class UploadFiles(models.Model):
    file = models.FileField(upload_to='file', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'upload_files'

    def __str__(self):
        return str(self.created_at)

    def save(self, *args, **kwargs):
        super(UploadFiles, self).save(*args, **kwargs)

    @property
    def file_url(self):
        # "Returns the image url."
        if self.file:
            return '%s%s' % (settings.HOST, self.file.url)
        return ''