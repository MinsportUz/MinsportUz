from rest_framework import serializers
from rest_framework.reverse import reverse
from admin_panel.model import press_service
from django.conf import settings


class TagSerializer(serializers.RelatedField):
    def to_representation(self, value):
        obj = {
            'id': value.id,
            'title': value.title,
            'slug': value.slug,
        }
        return obj


class NewsListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', required=False)
    category_slug = serializers.CharField(source='category.slug', required=False)

    class Meta:
        model = press_service.News
        fields = [
            'id', 'title', 'views', 'thumbnail_url', 'publish_date',
            'category', 'category_slug', 'actual'
        ]


class NewsTopSerializer(NewsListSerializer):
    thumbnail_url = serializers.CharField(source='cover_url')


class HeaderNewsSerializer(NewsListSerializer):
    class Meta:
        model = press_service.News
        fields = [
            'id', 'title'
        ]


class NewsDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', required=False)
    hashtag = TagSerializer(many=True, read_only=True)

    class Meta:
        model = press_service.News
        fields = [
            'id', 'title', 'description', 'short_description', 'image_url', 'views', 'publish_date',
            'category', 'hashtag',
        ]


class NewsCategoryserializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.NewsCategory
        fields = ['id', 'title', 'order', 'slug']


class NewsHashtagserializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.NewsHashtag
        fields = ['id', 'title', 'slug']


class PressSerializer(serializers.ModelSerializer):
    press = serializers.SerializerMethodField()

    class Meta:
        model = press_service.PressArticleLink
        fields = [
            'id', 'title', 'language', 'link', 'publish_date', 'press',
        ]

    def get_press(self, obj):
        if obj.press:
            payload = {
                'title': obj.press.title,
                'link': obj.press.link,
                'icon': obj.press.icon_url,
            }
            return payload


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.FAQ
        fields = [
            'id', 'title', 'description',
        ]


class NewsIntegration(serializers.Serializer):
    id = serializers.IntegerField()
    post_id = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()
    reach = serializers.SerializerMethodField()
    impressions = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    def get_post_id(self, obj):
        return obj.id

    def get_type(self, obj):
        return ''

    def get_created(self, obj):
        return obj.created_at

    def get_url(self, obj):
        frontend = 'https://minsport.uz/news/post/'
        url = frontend + str(obj.id)
        return url

    def get_text(self, obj):
        return obj.short_description

    def get_reactions(self, obj):
        return {
            "reactions": 0,
            "likes": 0,
            "views": obj.views,
            "comments": 0,
            "reposts": 0,
            "fallowers": 0,
        }

    def get_reach(self, obj):
        return {}

    def get_impressions(self, obj):
        return {}

    def get_categories(self, obj):
        return []


class AdmNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.News
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category_title_uz'] = instance.category.title_uz
        response['category_title_sr'] = instance.category.title_sr
        response['category_title_ru'] = instance.category.title_ru
        response['category_title_en'] = instance.category.title_en
        response['image'] = instance.image_url
        response['thumbnail'] = instance.thumbnail_url
        response['cover'] = instance.cover_url
        return response


class AdmNewsSMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.NewsSMedia
        fields = "__all__"


class AdmMediaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.MediaImage
        fields = "__all__"


class AdmNewsHashtagSerializer(serializers.ModelSerializer):
    usage_count = serializers.SerializerMethodField()
    class Meta:
        model = press_service.NewsHashtag
        fields = "__all__"

    def get_usage_count(self, instance):
        # Use the related manager to get the count of news that use this hashtag
        return instance.news.all().count()


class AdmNewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.NewsCategory
        fields = "__all__"


class AdmPhotoGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.PhotoGallery
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['images_count'] = instance.images.count()
        return response


class AdmPhotoGalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.PhotoGalleryImage
        fields = "__all__"


class AdmVideoGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.VideoGallery
        fields = "__all__"


class AdmPressSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.Press
        fields = "__all__"


class AdmPressArticleLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.PressArticleLink
        fields = "__all__"


class AdmFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.FAQ
        fields = "__all__"
