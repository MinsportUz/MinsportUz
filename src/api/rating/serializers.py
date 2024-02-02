from rest_framework import serializers
from admin_panel.model import rating
from django.conf import settings


class ParticipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = rating.Participants
        fields = '__all__'


class EvolutionCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = rating.EvolutionCriteria
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=False)
    class Meta:
        model = rating.Vote
        fields = ('participant', 'evolution_criteria', 'code')


class ParticipantsFilterSerializer(serializers.ModelSerializer):
    search = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = rating.Participants
        fields = ('search', 'region', 'district', 'organization')


class ParticipantsListSerializer(serializers.ModelSerializer):
    region_id = serializers.IntegerField(source='region.id')
    region_name = serializers.CharField(source='region.title')
    district_id = serializers.IntegerField(source='district.id')
    district_name = serializers.CharField(source='district.title')
    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = rating.Participants
        fields = (
            'id', 'firstname', 'lastname', 'position', 'created_at',
            'region_id', 'region_name', 'district_id', 'district_name', 'organization', 'image_url')

    def get_image_url(self, obj):
        # "Returns the image url."
        if obj.image:
            return '%s%s' % (settings.HOST, obj.image.url)
        return ''


class BotLinkSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = rating.Participants
        fields = ('code',)


class SubscribersSerializer(serializers.ModelSerializer):
    chat_id = serializers.IntegerField(required=False)
    code = serializers.CharField(required=False)
    fullname = serializers.CharField(required=False)

    class Meta:
        model = rating.Participants
        fields = ('chat_id', 'code', 'fullname')
