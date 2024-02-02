from rest_framework import serializers
from admin_panel.model import sport


class StadionSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source='region.title', required=False, read_only=True)

    class Meta:
        model = sport.Stadion
        fields = [
            'id', 'title', 'description', 'address',
            'region', 'host_team', 'established', 'capacity', 'image_url',
        ]


class ChampionSerializer(serializers.ModelSerializer):
    sport = serializers.CharField(source='sport.title', read_only=True, required=False)

    class Meta:
        model = sport.Champion
        fields = [
            'id', 'title', 'sport', 'competition',
            'image_url', 'medal', 'description',
        ]


class AdmStadionSerializer(serializers.ModelSerializer):
    class Meta:
        model = sport.Stadion
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['region_title_uz'] = instance.region.title_uz
        data['region_title_ru'] = instance.region.title_ru
        data['region_title_en'] = instance.region.title_en
        return data


class AdmSportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = sport.SportType
        fields = "__all__"



class AdmChampionSerializer(serializers.ModelSerializer):
    class Meta:
        model = sport.Champion
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['sport_title_uz'] = instance.sport.title_uz
        data['sport_title_ru'] = instance.sport.title_ru
        data['sport_title_en'] = instance.sport.title_en
        return data