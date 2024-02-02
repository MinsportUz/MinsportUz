from django.db import models
from django.utils import timezone
# from django.utils.translation import ugettext_lazy as _
# from django.utils.translation import gettext_lazy as _

from admin_panel.common import generate_field


class Vacancy(models.Model):
    title = models.CharField(max_length=500)
    education = models.ForeignKey('Education', on_delete=models.CASCADE, related_name='vacancy', null=True)
    employment = models.ForeignKey('Employment', on_delete=models.CASCADE, related_name='vacancy', null=True)
    about = models.TextField()
    tasks = models.TextField()

    count = models.IntegerField(default=1)
    date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vacancy'
        ordering = ['-date']

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.about_uz:
            self.about_sr = generate_field(self.about_uz)
        if self.tasks_uz:
            self.tasks_sr = generate_field(self.tasks_uz)

        super(Vacancy, self).save(*args, **kwargs)


class Education(models.Model):
    title = models.CharField(max_length=500)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'education'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(Education, self).save(*args, **kwargs)


class Employment(models.Model):
    title = models.CharField(max_length=500)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'employment'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(Employment, self).save(*args, **kwargs)
