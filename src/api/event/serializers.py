from rest_framework import serializers
from admin_panel.model import event
from api.views import RegionSerializer


class TagSerializer(serializers.RelatedField):
    def to_representation(self, value):
        obj = {
            'id': value.id,
            'title': value.title,
            'slug': value.slug,
        }
        return obj


class EventSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source='region.title', required=False)
    type = serializers.CharField(source='type.title')

    # event_date = serializers.DateTimeField(format='%d %B %Y', required=False, read_only=True)

    class Meta:
        model = event.Event
        fields = [
            'id', 'title', 'views', 'description', 'address', 'event_place',
            'image_url', 'event_date', 'region', 'type', 'expired'
        ]


class EventDetailSerializer(EventSerializer):
    hashtag = TagSerializer(many=True, read_only=True)

    class Meta:
        model = event.Event
        fields = [
            'id', 'title', 'views', 'link', 'description', 'address', 'event_place',
            'image_url', 'event_date', 'region', 'type', 'expired', 'hashtag',
        ]


class IndexEventSerializer(serializers.ModelSerializer):
    # event_date = serializers.DateTimeField(format='%d %B %Y', required=False, read_only=True)
    region = serializers.CharField(source='region.title', required=False)

    class Meta:
        model = event.Event
        fields = [
            'id', 'title', 'event_place', 'image_url', 'event_date', 'description', 'region',
        ]


class AdmEventSerializer(serializers.ModelSerializer):
    # event_date = serializers.DateTimeField(format='%d %B %Y', required=False, read_only=True)
    title_uz = serializers.CharField()
    title_ru = serializers.CharField()
    title_en = serializers.CharField()

    event_place_uz = serializers.CharField()
    event_place_ru = serializers.CharField()
    event_place_en = serializers.CharField()

    description_uz = serializers.CharField()
    description_ru = serializers.CharField()
    description_en = serializers.CharField()

    address_uz = serializers.CharField()
    address_ru = serializers.CharField()
    address_en = serializers.CharField()

    class Meta:
        model = event.Event
        fields = [
            'id', 'title_uz', 'title_ru', 'title_en', 'event_place_uz', 'event_place_ru', 'event_place_en',
            'event_date', 'description_uz', 'description_ru', 'description_en', 'address_uz',
            'address_ru', 'address_en', 'region', 'type', 'expired', 'link', 'hashtag', 'image',
            'is_published', 'views',
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['region_title_uz'] = instance.region.title_uz
        data['region_title_ru'] = instance.region.title_ru
        data['region_title_en'] = instance.region.title_en
        data['type_title_uz'] = instance.type.title_uz
        data['type_title_ru'] = instance.type.title_ru
        data['type_title_en'] = instance.type.title_en
        return data