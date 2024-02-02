from django.conf import settings
from django.db import models
from .territorial import Region, District
from .ministry import Organization


class Participants(models.Model):
    firstname = models.CharField(max_length=150, blank=True)
    lastname = models.CharField(max_length=150, blank=True)
    middlename = models.CharField(max_length=150, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=150, null=True)
    position = models.CharField(max_length=150, null=True)
    education = models.CharField(max_length=150, null=True)
    experience = models.CharField(max_length=150, null=True)
    phone = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='participants', blank=False, null=True)

    class Meta:
        db_table = 'participant'

    def __str__(self):
        return str(self.firstname)

    @property
    def image_url(self):
        # "Returns the image url."
        if self.image:
            return '%s%s' % (settings.HOST, self.image.url)
        return ''


class EvolutionCriteria(models.Model):
    title = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False, blank=True)
    image = models.ImageField(upload_to='evolution_criteria', null=True, blank=False)

    class Meta:
        db_table = 'evolution_criteria'

    def __str__(self):
        return str(self.title)


class UnicalCode(models.Model):
    code = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vote_unical_code'

    def __str__(self):
        return str(self.code)


class Subscribers(models.Model):
    chat_id = models.BigIntegerField(null=True, blank=True)
    unical_code = models.ForeignKey(UnicalCode, on_delete=models.CASCADE, null=True, blank=True)
    fullname = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vote_subscribers'

    def __str__(self):
        return str(self.chat_id)


class Vote(models.Model):
    participant = models.ForeignKey(Participants, on_delete=models.CASCADE, null=True, blank=True)
    evolution_criteria = models.ForeignKey(EvolutionCriteria, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subscriber = models.ForeignKey(Subscribers, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'vote'

    def __str__(self):
        return str(self.score)
