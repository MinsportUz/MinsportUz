from rest_framework import serializers

from admin_panel.model import tender


class TenderSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='type.title', required=False, read_only=True)
    primary_color = serializers.CharField(source='type.primary', required=False, read_only=True)
    region = serializers.CharField(source='region.title')

    class Meta:
        model = tender.Tender
        fields = [
            'id', 'title', 'date', 'number', 'organizer', 'file_url',
            'type', 'primary_color', 'region'
        ]


class AdmTypeSerializer(serializers.ModelSerializer):
    title_uz = serializers.CharField()
    title_ru = serializers.CharField()
    title_en = serializers.CharField()

    class Meta:
        model = tender.Type
        fields = ['id', 'title', 'primary', 'title_uz', 'title_ru', 'title_en']


class AdmTenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = tender.Tender
        fields = [
            'id', 'title', 'date', 'number', 'organizer', 'file_url',
            'title_uz', 'title_ru', 'title_en',
            'organizer_uz', 'organizer_ru', 'organizer_en',
            'type', 'region', 'is_published', 'created_at', 'file', 'date'
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['type_title_uz'] = instance.type.title_uz
        response['type_title_ru'] = instance.type.title_ru
        response['type_title_en'] = instance.type.title_en
        response['region_title_uz'] = instance.region.title_uz
        response['region_title_ru'] = instance.region.title_ru
        response['region_title_en'] = instance.region.title_en
        return response


class AdmTenderNoticesSerializer(serializers.ModelSerializer):

    class Meta:
        model = tender.TenderNotices
        fields = ['id', 'built_year', 'created_at', 'title', 'address', 'land_area', 'size', 'status'
                  'title_uz', 'title_ru', 'title_en', 'address_uz', 'address_ru', 'address_en', 'land_area_uz',
                  'land_area_ru', 'land_area_en', 'size_uz', 'size_ru', 'size_en', 'status_uz', 'status_ru', 'number',
                  'status_en', 'is_published', ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['photos'] = AdmTenderNoticesPhotosSerializer(
            tender.TenderNoticesPhotos.objects.filter(tender=instance.id), many=True).data
        return response


class TenderNoticesSerializer(serializers.ModelSerializer):

    class Meta:
        model = tender.TenderNotices
        fields = ['id', 'title', 'address', 'land_area', 'size', 'status', 'built_year',
                  'is_published']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['photos'] = AdmTenderNoticesPhotosSerializer(
            tender.TenderNoticesPhotos.objects.filter(tender=instance.id), many=True).data
        return response


class AdmTenderNoticesPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = tender.TenderNoticesPhotos
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['image'] = instance.image_url
        return response
