from django.utils.timezone import now
from rest_framework import serializers
from admin_panel.model import service, ministry


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = service.Service
        fields = [
            'id', 'title', 'order', 'icon_url', 'url'
        ]


class AdmServiceSerializer(serializers.ModelSerializer):
    title_uz = serializers.CharField()
    title_ru = serializers.CharField()
    title_en = serializers.CharField()

    class Meta:
        model = service.Service
        fields = "__all__"


class EmployeeRatingPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = service.EmployeeRating
        fields = [
            'id', 'region', 'district', 'organization', 'employee', 'service_type', 'grade_type'
        ]


class EmployeeRatingOverallSerializer(serializers.ModelSerializer):
    class Meta:
        model = service.EmployeeRating
        fields = [
            ''
        ]


# class InstitutionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = service.Institutions
#         fields = '__all__'


# class InstitutionsItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = service.InstitutionItem
#         fields = '__all__'
#
#     def update(self, instance, validated_data):
#         instance = super().update(instance, validated_data)
#         instance.updated_at = now()
#         instance.save()
#         return instance
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['staff'] = instance.staff.title if instance.staff else ''
#         representation['sport_type'] = instance.sport_type.title if instance.sport_type else ''
#         representation['image'] = instance.image_url()
#         return representation
#
#
# class InstitutionsGetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = service.Institutions
#         fields = '__all__'
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         items = service.InstitutionItem.objects.filter(institution=instance.id)
#         representation['items'] = InstitutionsItemSerializer(items, many=True).data
#         return representation
