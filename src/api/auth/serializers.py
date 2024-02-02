from rest_framework import serializers
from admin_panel.model import ministry, vacancy
from admin_panel.model.service import EmployeeRating
from django.conf import settings
from django.db.models import Count, Avg
from django.contrib.auth.models import Group, Permission,User
from admin_panel.model.user import CustomUser


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
            'title', 'content'
        ]


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'