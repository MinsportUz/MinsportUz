from rest_framework import serializers
from rest_framework import serializers

from admin_panel.model import event, press_service, static


class MediaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.MediaImage
        fields = ['image']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = event.Event
        fields = ('id', 'title')


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.News
        fields = ('id', 'title')


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.PhotoGallery
        fields = ('id', 'title')


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.VideoGallery
        fields = ('id', 'title')


class StaticSerializer(serializers.ModelSerializer):
    class Meta:
        model = static.StaticPage
        fields = ('id', 'title', 'url', 'slug')


class SearchSerializer(serializers.Serializer):
    events = EventSerializer(many=True)
    news = NewsSerializer(many=True)
    photogallery = PhotoSerializer(many=True)
    videogallery = VideoSerializer(many=True)
    static_page = StaticSerializer(many=True)
