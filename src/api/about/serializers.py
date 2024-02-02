from rest_framework import serializers
from admin_panel.model import ministry, vacancy
from admin_panel.model.service import EmployeeRating
from django.conf import settings
from django.db.models import Count, Avg

from api.views import RegionSerializer


class StatSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = ministry.MinistryStat
        fields = ['title', 'count', 'icon', 'colour']

    def get_icon(self, obj):
        if obj.icon:
            return settings.HOST + '' + obj.icon.url


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.Staff
        fields = [
            'title', 'position', 'work_history', 'duty',
        ]


class AboutUsSerializer(serializers.ModelSerializer):
    leader = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = ministry.AboutMinistry
        fields = [
            'content', 'image', 'leader',
        ]

    def get_leader(self, obj):
        staff = ministry.Staff.objects.filter(main=True, leader=True).first()
        return DirectorSerializer(staff).data

    def get_image(self, obj):
        if obj.image:
            return settings.HOST + '' + obj.image.url


class AboutSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ministry.AboutMinistry
        fields = ['content', 'image']

    def get_image(self, obj):
        if obj.image:
            return settings.HOST + '' + obj.image.url


class StructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.MinistryStructure
        fields = [
            'title', 'content',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = instance.image_url
        return representation


class DepartmentSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    leader = serializers.SerializerMethodField()

    class Meta:
        model = ministry.Department
        fields = [
            'id', 'title', 'address', 'lat', 'long',
            'region', 'phone_number', 'type',
            'email', 'link',
            'instagram', 'telegram', 'facebook', 'twitter',
            'leader',
        ]

    def get_leader(self, obj):
        staff = ministry.Staff.objects.filter(leader=False, department=obj).last()
        result = {
            'name': '',
            'reception_days': '',
        }
        if staff:
            result = {
                'name': staff.title,
                'reception_days': staff.reception_days,
            }
            # return result
            return result
        return result


class VacancySerializer(serializers.ModelSerializer):
    education = serializers.CharField(source='education.title', required=False)
    employment = serializers.CharField(source='employment.title', required=False)

    class Meta:
        model = vacancy.Vacancy
        fields = [
            'id', 'title', 'education', 'employment',
            'about', 'tasks', 'count', 'date',
        ]


class OrganizationListSerializer(DepartmentSerializer):
    """Inherited DepartmentSerializer above. So left some code in department's serializers"""
    leader = serializers.SerializerMethodField()

    class Meta:
        model = ministry.Organization
        fields = [
            'id', 'title', 'leader'
        ]

    def get_leader(self, obj):
        staff = ministry.Staff.objects.filter(leader=False, organization=obj).last()
        result = {
            'leader_id': '',
            'name': '',
        }
        if staff:
            result = {
                'id': staff.id,
                'name': staff.title,
            }
            # return result
            return result
        return result


class OrganizationDetailSerializer(DepartmentSerializer):
    """Inherited DepartmentSerializer above. So left some code in department's serializers"""
    rating_result = serializers.SerializerMethodField()

    class Meta:
        model = ministry.Organization
        fields = [
            'id', 'title', 'rating_result'
        ]

    def get_rating_result(self, obj):
        organization_ratings = EmployeeRating.objects.filter(organization=obj)
        organization_ratings_service_types = organization_ratings.values('service_type') \
                                                 .annotate(total_count=Count('id'),
                                                           avg_grade=Avg('grade_type')) \
                                                 .order_by('-total_count', '-avg_grade')[:3]
        service_summary = []
        for service in organization_ratings_service_types:
            service_name = dict(EmployeeRating.service_choice).get(service['service_type'])
            service_summary.append({'service_type': service_name,
                                    'total_count': service['total_count'],
                                    'avg_grade': round(service['avg_grade'], 1)})
        return service_summary


class StaffSerializer(serializers.ModelSerializer):
    # department = serializers.SerializerMethodField()
    # organization = serializers.SerializerMethodField()
    # department = DepartmentSerializer()

    class Meta:
        model = ministry.Staff
        fields = [
            'id', 'title', 'position', 'inner_phone_number', 'reception_days',
            'work_history', 'duty', 'email', 'image',
            'leader', 'main',
            'twitter', 'facebook', 'telegram', 'instagram'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = instance.image_url
        return representation

    # def get_organization(self, obj):
    #     if obj.organization:
    #         return obj.organization.title
    #
    # def get_department(self, obj):
    #     if obj.department:
    #         return obj.department.title


class StaffCentralSerializer(StaffSerializer):
    class Meta:
        model = ministry.Staff
        fields = [
            'id', 'title', 'position', 'inner_phone_number',
            'work_history', 'duty', 'email', 'image',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = instance.image_url
        return representation

class StaffRegionalSerializer(serializers.ModelSerializer):
    # department = DepartmentSerializer()
    department = serializers.SerializerMethodField()

    class Meta:
        model = ministry.Staff
        fields = [
            'id', 'title', 'position', 'inner_phone_number', 'reception_days',
            'work_history', 'duty', 'email', 'image',
            'department',
            'leader', 'main', 'is_central',
            'twitter', 'facebook', 'telegram', 'instagram'
        ]

    def get_department(self, obj):
        if obj.department:
            result = {
                'address': '%s, %s' % (obj.department.region.title, obj.department.address),
                'region_slug': obj.department.region.slug,
                'region': obj.department.region.image_url,
            }
            return result

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = instance.image_url
        return representation


class StaffOrganizationSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()

    class Meta:
        model = ministry.Staff
        fields = [
            'id', 'title', 'position', 'inner_phone_number', 'reception_days',
            'work_history', 'duty', 'email',
            'organization',
        ]

    def get_organization(self, obj):
        if obj.organization:
            result = {
                'address': '%s, %s' % (obj.organization.region.title, obj.organization.address),
                'image': obj.organization.image_url
            }
            return result


class AdmAboutMinistrySerializer(serializers.ModelSerializer):
    content_uz = serializers.CharField()
    content_ru = serializers.CharField()
    content_en = serializers.CharField()

    class Meta:
        model = ministry.AboutMinistry
        fields = [
            'id', 'content', 'image', 'content_uz', 'content_ru', 'content_en'
        ]


class AdmMinistryStructureSerializer(serializers.ModelSerializer):
    # content_uz = serializers.CharField()
    # content_ru = serializers.CharField()
    # content_en = serializers.CharField()
    #
    # title_uz = serializers.CharField()
    # title_ru = serializers.CharField()
    # title_en = serializers.CharField()

    class Meta:
        model = ministry.MinistryStructure
        fields = [
            'id', 'title', 'image'
        ]


class AdmMinistryStatSerializer(serializers.ModelSerializer):
    title_uz = serializers.CharField()
    title_ru = serializers.CharField()
    title_en = serializers.CharField()

    class Meta:
        model = ministry.MinistryStat
        fields = [
            'id', 'title', 'colour', 'count', 'icon', 'title_uz', 'title_ru', 'title_en'
        ]


class AdmMinistryStaffSerializer(serializers.ModelSerializer):
    title_uz = serializers.CharField()
    title_ru = serializers.CharField()
    title_en = serializers.CharField()

    class Meta:
        model = ministry.Staff
        fields = "__all__"

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'title': instance.title,
            'title_uz': instance.title_uz,
            'title_ru': instance.title_ru,
            'title_en': instance.title_en,
            'position': instance.position,
            'position_uz': instance.position_uz,
            'position_ru': instance.position_ru,
            'position_en': instance.position_en,
            'inner_phone_number': instance.inner_phone_number,
            'reception_days': instance.reception_days,
            'reception_days_uz': instance.reception_days_uz,
            'reception_days_ru': instance.reception_days_ru,
            'reception_days_en': instance.reception_days_en,
            'work_history': instance.work_history,
            'work_history_uz': instance.work_history_uz,
            'work_history_ru': instance.work_history_ru,
            'work_history_en': instance.work_history_en,
            'duty_uz': instance.duty_uz,
            'duty_ru': instance.duty_ru,
            'duty_en': instance.duty_en,
            'duty': instance.duty,
            'email': instance.email,
            'image': instance.image_url,
            'leader': instance.leader,
            'main': instance.main,
            'is_central': instance.is_central,
            'twitter': instance.twitter,
            'facebook': instance.facebook,
            'telegram': instance.telegram,
            'instagram': instance.instagram,
            'order': instance.order,
            'department': instance.department.id if instance.department else None,
            'organization': instance.organization.title if instance.organization else None,
            'organization_id': instance.organization.id if instance.organization else None,
            'department_uz': instance.department.title_uz if instance.department else None,
            'department_ru': instance.department.title_ru if instance.department else None,
            'department_en': instance.department.title_en if instance.department else None,
            'organization_uz': instance.organization.title_uz if instance.organization else None,
            'organization_ru': instance.organization.title_ru if instance.organization else None,
            'organization_en': instance.organization.title_en if instance.organization else None,
        }


class AdmMinistryDepartmentSerializer(serializers.ModelSerializer):
    title_uz = serializers.CharField()
    title_ru = serializers.CharField()
    title_en = serializers.CharField()

    class Meta:
        model = ministry.Department
        fields = "__all__"

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'title': instance.title,
            'title_uz': instance.title_uz,
            'title_ru': instance.title_ru,
            'title_en': instance.title_en,
            'address': instance.address,
            'address_uz': instance.address_uz,
            'address_ru': instance.address_ru,
            'address_en': instance.address_en,
            'region': instance.region.id,
            'region_uz': instance.region.title_uz,
            'region_ru': instance.region.title_ru,
            'region_en': instance.region.title_en,
            'phone_number': instance.phone_number,
            'link': instance.link,
            'email': instance.email,
            'long': instance.long,
            'lat': instance.lat,
            'instagram': instance.instagram,
            'telegram': instance.telegram,
            'facebook': instance.facebook,
            'twitter': instance.twitter,
            'updated_at': instance.updated_at,
            'created_at': instance.created_at,
        }


class AdmOrganizationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.OrganizationType
        fields = "__all__"


class AdmMinistryOrganizationSerializer(serializers.ModelSerializer):
    title_uz = serializers.CharField()
    title_ru = serializers.CharField()
    title_en = serializers.CharField()

    class Meta:
        model = ministry.Organization
        fields = "__all__"

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'title': instance.title,
            'title_uz': instance.title_uz,
            'title_ru': instance.title_ru,
            'title_en': instance.title_en,
            'address': instance.address,
            'address_uz': instance.address_uz,
            'address_ru': instance.address_ru,
            'address_en': instance.address_en,
            'region': instance.region.id,
            'region_uz': instance.region.title_uz,
            'region_ru': instance.region.title_ru,
            'region_en': instance.region.title_en,
            'district': instance.district.id if instance.district else None,
            'district_uz': instance.district.title_uz if instance.district else None,
            'district_ru': instance.district.title_ru if instance.district else None,
            'district_en': instance.district.title_en if instance.district else None,
            'organization_type': instance.organization_type.id if instance.organization_type else None,
            'organization_type_uz': instance.organization_type.title_uz if instance.organization_type else None,
            'organization_type_ru': instance.organization_type.title_ru if instance.organization_type else None,
            'organization_type_en': instance.organization_type.title_en if instance.organization_type else None,
            'phone_number': instance.phone_number,
            'link': instance.link,
            'image': instance.image.image_url if instance.image else None,
            'email': instance.email,
            'long': instance.long,
            'lat': instance.lat,
            'instagram': instance.instagram,
            'telegram': instance.telegram,
            'facebook': instance.facebook,
            'twitter': instance.twitter,
            'updated_at': instance.updated_at,
            'created_at': instance.created_at,
        }


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.Organization
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['update_at'] = instance.updated_at.strftime("%d.%m.%Y")
        representation['leader'] = ministry.Staff.objects.filter(organization=instance).first().title if ministry.Staff.objects.filter(organization=instance).first() else None
        representation['image_url'] = instance.image.image_url if instance.image else None
        return representation


class OrganizationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.OrganizationType
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['items'] = OrganizationSerializer(instance.organization_set.all(), many=True).data
        return representation


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.Visitor
        fields = "__all__"


class AdmCarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.Cars
        fields = "__all__"

    def to_representation(self, instance):
        responce = super().to_representation(instance)
        responce['car_type_uz'] = instance.car_type.title_uz
        responce['car_type_ru'] = instance.car_type.title_ru
        responce['car_type_en'] = instance.car_type.title_en
        return responce


class AdmCarBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.Cars
        fields = "__all__"

    def to_representation(self, instance):
        responce = {}
        responce['id'] = instance.id
        responce['model_uz'] = instance.model_uz
        responce['model_ru'] = instance.model_ru
        responce['model_en'] = instance.model_en
        responce['car_type_uz'] = instance.car_type.title_uz
        responce['car_type_ru'] = instance.car_type.title_ru
        responce['car_type_en'] = instance.car_type.title_en
        responce['comment_uz'] = instance.comment_uz
        responce['comment_ru'] = instance.comment_ru
        responce['comment_en'] = instance.comment_en
        responce['number'] = instance.number
        responce['staff_position_uz'] = instance.staff.position_uz
        responce['staff_position_ru'] = instance.staff.position_ru
        responce['staff_position_en'] = instance.staff.position_en
        return responce


class AdmCarInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.CarInfo
        fields = "__all__"

    def to_representation(self, instance):
        responce = super().to_representation(instance)
        cars = ministry.Cars.objects.all()
        responce['cars'] = AdmCarBaseSerializer(cars, many=True).data
        return responce


class CarBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.Cars
        fields = "__all__"

    def to_representation(self, instance):
        responce = {}
        responce['id'] = instance.id
        responce['model'] = instance.model
        responce['car_type'] = instance.car_type.title
        responce['comment'] = instance.comment
        responce['number'] = instance.number
        responce['staff_position'] = instance.staff.position
        return responce


class CarInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.CarInfo
        fields = "__all__"

    def to_representation(self, instance):
        responce = {}
        language = self.context.get('language')
        if language == 'oz':
            responce['content'] = instance.content
            responce['title'] = instance.title
        elif language == 'ru':
            responce['content'] = instance.content_ru
            responce['title'] = instance.title_ru
        elif language == 'en':
            responce['content'] = instance.content_en
            responce['title'] = instance.title_en
        else:
            responce['content'] = instance.content_sr
            responce['title'] = instance.title_sr
        responce['id'] = instance.id
        responce['code'] = instance.code
        responce['created_at'] = instance.created_at
        responce['publish_date'] = instance.publish_date
        cars = ministry.Cars.objects.all()
        responce['cars'] = CarBaseSerializer(cars, many=True).data
        return responce
