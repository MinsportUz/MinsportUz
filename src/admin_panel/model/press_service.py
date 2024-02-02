from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
# from django.utils.translation import ugettext_lazy as _
# from sorl.thumbnail import ImageField
from django_resized import ResizedImageField
from django.db.models.signals import post_save, pre_save

from admin_panel.common import generate_field
from admin_panel.model import territorial

# Image cropping conf
THUMBNAIL = [300, 170]
IMAGE = [1200, 675]
COVER = [1200, 675]


def generate_unique_slug(klass, field):
    """
    return unique slug if origin slug is exist.
    eg: `foo-bar` => `foo-bar-1`

    :param `klass` is Class model.
    :param `field` is specific field for title.
    """
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return unique_slug


class News(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    thumbnail = ResizedImageField(size=THUMBNAIL, upload_to='news')
    image = ResizedImageField(size=IMAGE, upload_to='news')
    cover = ResizedImageField(upload_to='news', size=COVER)
    video_link = models.URLField(null=True, blank=True)
    views = models.IntegerField(default=0)
    category = models.ForeignKey('NewsCategory', on_delete=models.CASCADE, related_name='news')
    hashtag = models.ManyToManyField('NewsHashtag', related_name='news', blank=True)
    region = models.ForeignKey('Region', related_name='news', on_delete=models.CASCADE, blank=True, null=True)
    main_page = models.BooleanField(default=False)
    actual = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'news'
        ordering = ['-publish_date']

    def __str__(self):
        return str(self.title)

    @property
    def thumbnail_url(self):

        # "Returns the image url."
        return '%s%s' % (settings.HOST, self.thumbnail.url) if self.thumbnail else ''

    @property
    def image_url(self):

        # "Returns the image url."
        return '%s%s' % (settings.HOST, self.image.url) if self.image else ""

    @property
    def facebook(self):

        # "Returns the image url."
        item = NewsSMedia.objects.filter(news=self.id)
        if item.exists():
            return item.first().facebook
        return False

    @property
    def telegram(self):

        # "Returns the image url."
        item = NewsSMedia.objects.filter(news=self.id)
        if item.exists():
            return item.first().telegram
        return False

    @property
    def cover_url(self):
        return '%s%s' % (settings.HOST, self.cover.url) if self.cover else ""

    # def save(self, *args, **kwargs):
    #     if self.title_uz:
    #         self.title_sr = generate_field(self.title_uz)
    #     if self.description_uz:
    #         self.description_sr = generate_field(self.description_uz)
    #     if self.short_description_uz:
    #         self.short_description_sr = generate_field(self.short_description_uz)
    #
    #     super(News, self).save(*args, **kwargs)


class NewsSMedia(models.Model):
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='smedia')
    facebook = models.BooleanField(default=False)
    telegram = models.BooleanField(default=False)

    class Meta:
        db_table = 'news_smedia'

    def save(self, *args, **kwargs):
        super(NewsSMedia, self).save(*args, **kwargs)


class MediaImage(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = ResizedImageField(size=IMAGE, upload_to='uploads')
    cover = ResizedImageField(upload_to='uploads/cover/', size=COVER)

    def __str__(self):
        return str(self.created_at)

    @property
    def image_url(self):
        # "Returns the image url."
        return '%s%s' % (settings.HOST, self.image.url) if self.image else ""

    @property
    def cover_url(self):
        return '%s%s' % (settings.HOST, self.cover.url) if self.cover else ""


class NewsHashtag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=200, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'news_hashtags'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title_en) != self.slug:
                self.slug = generate_unique_slug(NewsHashtag, self.title_en)
        else:  # create
            self.slug = generate_unique_slug(NewsHashtag, self.title_en)
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(NewsHashtag, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)


class NewsCategory(models.Model):
    title = models.CharField(max_length=500)
    order = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, max_length=200, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'news_categories'
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title_en) != self.slug:
                self.slug = generate_unique_slug(NewsCategory, self.title_en)
        else:  # create
            self.slug = generate_unique_slug(NewsCategory, self.title_en)
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(NewsCategory, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)


class PhotoGallery(models.Model):
    title = models.CharField(max_length=500)
    thumbnail = ResizedImageField(size=THUMBNAIL, upload_to='photo_gallery_thumbnails')
    views = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'photo_gallery'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.title)

    @property
    def thumbnail_url(self):
        # "Returns the image url."
        return '%s%s' % (settings.HOST, self.thumbnail.url) if self.thumbnail else ''

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(PhotoGallery, self).save(*args, **kwargs)


class PhotoGalleryImage(models.Model):
    photo_gallery = models.ForeignKey(PhotoGallery, on_delete=models.CASCADE, related_name='images')
    image = ResizedImageField(size=IMAGE, upload_to='photo_gallery')

    class Meta:
        db_table = 'photo_gallery_images'
        ordering = ['-id']

    def __str__(self):
        return self.image.name

    @property
    def url(self):
        # "Returns the image url."
        return '%s%s' % (settings.HOST, self.image.url)


class VideoGallery(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    thumbnail = ResizedImageField(size=THUMBNAIL, upload_to='video_gallery_thumbnails')
    video_link = models.URLField()
    views = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'video_gallery'
        ordering = ['-publish_date']

    def __str__(self):
        return str(self.title)

    @property
    def thumb(self):
        # "Returns the image url."
        return '%s%s' % (settings.HOST, self.thumbnail.url) if self.thumbnail else ''

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.description_uz:
            self.description_sr = generate_field(self.description_uz)

        super(VideoGallery, self).save(*args, **kwargs)


class Press(models.Model):
    title = models.CharField(max_length=500)
    link = models.URLField()
    icon = models.FileField(upload_to='icon')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'press'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.title)

    @property
    def icon_url(self):
        return '%s%s' % (settings.HOST, self.icon.url) if self.icon else ''


class PressArticleLink(models.Model):
    title = models.CharField(max_length=500)
    language = models.CharField(max_length=200)
    link = models.URLField()
    press = models.ForeignKey(Press, on_delete=models.CASCADE, related_name='article')
    is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'press_article_link'
        ordering = ['-publish_date']

    def __str__(self):
        return str(self.title)


class FAQ(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    order = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'faq'
        ordering = ['-order']

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)

        if self.description_uz:
            self.description_sr = generate_field(self.description_uz)

        super(FAQ, self).save(*args, **kwargs)
