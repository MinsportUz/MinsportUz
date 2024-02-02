from django.conf import settings
from rest_framework import serializers

from admin_panel.model import press_service, external


class GalleryImageSerializer(serializers.RelatedField):
    def to_representation(self, value):
        obj = {
            'id': value.id,
            'src': value.url,
        }
        return obj


class PhotoSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(source='images.count', read_only=True, required=False)

    class Meta:
        model = press_service.PhotoGallery
        fields = [
            'id', 'title', 'thumbnail_url', 'publish_date', 'count',
        ]


class PhotoDetailSerializer(serializers.ModelSerializer):
    images = GalleryImageSerializer(many=True, read_only=True)

    class Meta:
        model = press_service.PhotoGallery
        fields = [
            'id', 'title', 'views', 'publish_date', 'images',
        ]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.PhotoGalleryImage
        fields = ['id', 'url', 'photo_gallery']


class ExternalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = external.ExternalImage
        fields = ['id', 'url', 'image']

    def to_representation(self, value):
        representation = super().to_representation(value)
        representation['image_url'] = value.image_url
        return representation


class VideoSerializer(serializers.ModelSerializer):
    src = serializers.URLField(source='video_link')

    class Meta:
        model = press_service.VideoGallery
        fields = [
            'id', 'title', 'thumb', 'description', 'src',
            'views', 'publish_date'
        ]


class AdmExternalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = external.ExternalImage
        fields = '__all__'