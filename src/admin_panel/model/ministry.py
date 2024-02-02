from django.conf import settings
from django.db import models
# from sorl.thumbnail import ImageField
from django_resized import ResizedImageField

from admin_panel.common import generate_field
from admin_panel.model.territorial import Region, District

# Image cropping conf
THUMBNAIL = [300, 170]
IMAGE = [300, 300]


class AboutMinistry(models.Model):
    # title = models.CharField(max_length=500, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='minstry', null=True, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'about_ministry'

    def __str__(self):
        return str(self.content)

    def save(self, *args, **kwargs):
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        super(AboutMinistry, self).save(*args, **kwargs)


class MinistryStructure(models.Model):
    title = models.CharField(max_length=350)
    content = models.TextField()
    image = models.ImageField(upload_to='structure', null=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ministry_structure'

    def __str__(self):
        return str(self.title)

    @property
    def image_url(self):
        # "Returns the image url."
        if self.image:
            return '%s%s' % (settings.HOST, self.image.url)
        return ''

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        super(MinistryStructure, self).save(*args, **kwargs)


class MinistryStat(models.Model):
    title = models.CharField(max_length=350)
    colour = models.CharField(max_length=500, default='')
    count = models.IntegerField(default=0, blank=True)
    icon = models.FileField(upload_to='icon')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ministry_stat'
        ordering = ['-id']

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(MinistryStat, self).save(*args, **kwargs)


# General staff model (only BOOL fields will be filtered in view)
class Staff(models.Model):
    title = models.CharField(max_length=355)
    order = models.IntegerField(default=0)
    position = models.CharField(max_length=500, null=True, blank=True)
    inner_phone_number = models.CharField(max_length=50, null=True, blank=True)
    reception_days = models.CharField(max_length=255, null=True, blank=True)
    work_history = models.TextField(null=True, blank=True)
    duty = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    image = ResizedImageField(size=IMAGE, upload_to='staff', null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    telegram = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    main = models.BooleanField(default=False)
    leader = models.BooleanField(default=False)
    is_central = models.BooleanField(default=False)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True, related_name='staff')
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='staff')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'staff'
        ordering = ['order']

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)

        if self.position_uz:
            self.position_sr = generate_field(self.position_uz)

        # if self.reception_days_uz:
        # self.reception_days_sr = generate_field(self.reception_days_uz)

        if self.work_history_uz:
            self.work_history_sr = generate_field(self.work_history_uz)

        if self.duty_uz:
            self.duty_sr = generate_field(self.duty_uz)
        super(Staff, self).save(*args, **kwargs)

    @property
    def image_url(self):
        # "Returns the image url."
        if self.image:
            return '%s%s' % (settings.HOST, self.image.url)
        return ''


# Extra departments for STAFF
class Department(models.Model):
    title = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    link = models.CharField(max_length=200, null=True)
    email = models.EmailField()
    long = models.CharField(max_length=100, blank=True, null=True)
    lat = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.URLField(null=True, blank=True)
    telegram = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'departments'
        ordering = ['-region', 'created_at']

    def __str__(self):
        return str(self.title)

    @property
    def type(self):
        return 'department'

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.address_uz:
            self.address_sr = generate_field(self.address_uz)

        super(Department, self).save(*args, **kwargs)


class OrganizationType(models.Model):
    title = models.CharField(max_length=500, null=True, blank=False)
    url = models.TextField(null=True, blank=True)
    slug = models.CharField(max_length=25, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'organization_type'
        ordering = ['created_at']

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(OrganizationType, self).save(*args, **kwargs)


# Extra organization for STAFF
class Organization(models.Model):
    title = models.CharField(max_length=500)
    address = models.CharField(max_length=500, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    link = models.CharField(max_length=200, blank=True, null=True)
    image = ResizedImageField(size=IMAGE, upload_to='organization', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    long = models.CharField(max_length=100, blank=True, null=True)
    lat = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.URLField(null=True, blank=True)
    telegram = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    organization_type = models.ForeignKey(OrganizationType, on_delete=models.CASCADE, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'organizations'
        ordering = ['-region', 'created_at']

    def __str__(self):
        return str(self.title)

    @property
    def type(self):
        return 'organization'

    @property
    def image_url(self):
        # "Returns the image url."
        if self.image:
            return '%s%s' % (settings.HOST, self.image.url)
        return ''

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.address_uz:
            self.address_sr = generate_field(self.address_uz)

        super(Organization, self).save(*args, **kwargs)


class Visitor(models.Model):
    ip = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    browser = models.CharField(max_length=250, null=True, blank=True)
    os = models.CharField(max_length=100, null=True, blank=True)
    device = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'visitors'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.ip)


class VisitorLog(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    url = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'visitor_logs'
        indexes = [
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return str(self.url)


class CarInfo(models.Model):
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=500)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    publish_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'car_info'

    def __str__(self):
        return str(self.content)

    def save(self, *args, **kwargs):
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        super(CarInfo, self).save(*args, **kwargs)


class CarTypes(models.Model):
    title = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'car_types'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(CarTypes, self).save(*args, **kwargs)


class Cars(models.Model):
    car_type = models.ForeignKey(CarTypes, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    comment = models.TextField(null=True, blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cars'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.model)

    def save(self, *args, **kwargs):
        if self.model_uz:
            self.model_sr = generate_field(self.model_uz)
        if self.comment_uz:
            self.comment_sr = generate_field(self.comment_uz)
        super(Cars, self).save(*args, **kwargs)
