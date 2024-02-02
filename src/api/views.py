from django.shortcuts import render
from rest_framework import serializers, viewsets
from admin_panel.model import territorial


# Create your views here.
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = territorial.Region
        fields = [
            'id', 'title'
        ]


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = territorial.District
        fields = [
            'id', 'title', 'region'
        ]


class RegionDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = territorial.RegionalDepartment
        fields = [
            'id', 'title', 'phone_number', 
        ]