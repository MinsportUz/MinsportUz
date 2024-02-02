from rest_framework import serializers
from admin_panel.model import settings
from api.views import RegionSerializer, RegionDepartmentSerializer
from admin_panel.model import menu
from admin_panel.model import useful_link
from admin_panel.model import contact
from admin_panel.model import territorial


class SiteContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.ContactSetting
        fields = [
            'address', 'buses', 'mini_buses', 'bus_station',
            'metro_station', 'working_days', 'working_hours',
            'email', 'phone_number',
        ]


class HeaderSubMenuSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = menu.Menu
        fields = [
            'id', 'title', 'url', 'is_static'
        ]

    def get_url(self, obj):
        if obj.is_static:
            return 'static/' + obj.url
        else:
            return obj.url


class MenuSerializer(serializers.ModelSerializer):
    child = serializers.SerializerMethodField()

    class Meta:
        model = menu.Menu
        fields = [
            'id', 'title', 'url',
            'child',
        ]

    def get_child(self, obj):
        sub_menu = menu.Menu.objects.filter(parent=obj)
        if sub_menu.exists():
            return HeaderSubMenuSerializer(sub_menu, many=True).data
        return []


class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.MainPageSetting
        fields = [
            'logo_title', 'e_link', 'phone_number', 'icon_url', 'menu_icon_link',
            'updated_at',
        ]


class FooterSerializer(serializers.ModelSerializer):
    # site = HeaderSerializer()
    site = serializers.SerializerMethodField()

    class Meta:
        model = settings.ContactSetting
        fields = [
            'site',
            'instagram', 'telegram', 'facebook', 'twitter', 'youtube',
        ]

    def get_site(self, obj):
        return HeaderSerializer(settings.MainPageSetting.objects.last()).data


class UsefulLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = useful_link.UsefulLink
        fields = [
            'id', 'title', 'url', 'icon_url', 'description',
        ]


class AdmUsefulLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = useful_link.UsefulLink
        fields = '__all__'


class PosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.MainPageSetting
        fields = [
            'mobile_title', 'mobile_description', 'mobile_image_url',
            'mobile_poster_url', 'mobile_android', 'mobile_ios',
            'home_ad_url', 'home_ad_android', 'home_ad_ios',
            'poster_link', 'poster_url',
        ]


class MenuDevSerializer(serializers.ModelSerializer):
    child = serializers.SerializerMethodField()

    class Meta:
        model = menu.Menu
        fields = [
            'id', 'title', 'url',
            'parent', 'child'
        ]

    #
    def get_child(self, obj):
        sub_menu = menu.Menu.objects.filter(parent=obj)
        if sub_menu.exists():
            return HeaderSubMenuSerializer(sub_menu, many=True).data
        return []


class AdmMainPageSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.MainPageSetting
        fields = '__all__'


class AdmContactSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.ContactSetting
        fields = '__all__'


class AdmTypoSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.Typo
        fields = '__all__'


class AdmReceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = contact.Reception
        fields = '__all__'


class AdmRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = territorial.Region
        fields = '__all__'


class AdmDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = territorial.District
        fields = '__all__'


class AdmRegionDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = territorial.RegionalDepartment
        fields = '__all__'
