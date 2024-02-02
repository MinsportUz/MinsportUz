import django_filters.filterset
from django.utils.timezone import now
from rest_framework import viewsets, status, generics
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from admin_panel.model import ministry, menu
from admin_panel.model import vacancy
from . import serializers
from .. import pagination
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from api.static.serializers import StaticMenuSerializer
from django.utils.translation import activate
import requests


class CustomModalViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')
        return queryset


class AboutUsView(CustomModalViewSet):
    queryset = ministry.AboutMinistry.objects.all()
    serializer_class = serializers.AboutUsSerializer
    pagination_class = None
    http_method_names = ['get']

    def list(self, request):
        stat = serializers.StatSerializer(ministry.MinistryStat.objects.all(), many=True).data
        about = serializers.AboutUsSerializer(self.get_queryset(), many=True).data
        dict = {
            'about': about,
            'stat': stat,
        }
        return Response(dict, status=status.HTTP_200_OK)


class StructureView(CustomModalViewSet):
    queryset = ministry.MinistryStructure.objects.all()
    serializer_class = serializers.StructureSerializer
    pagination_class = None
    http_method_names = ['get', ]

    def list(self, request, *args, **kwargs):
        lang = request.headers.get('Accept-Language')
        if lang:
            activate(lang)
        else:
            activate('ru')
        instance = self.get_queryset()
        serializer = self.serializer_class
        structure = serializer(instance, many=True).data
        menu_serializer = StaticMenuSerializer
        page_menu = menu.Menu.objects.filter(url='ministry')
        if page_menu.exists():
            parent_menu = page_menu.first()
            result = menu.Menu.objects.filter(parent=parent_menu)
        else:
            parent_menu = menu.Menu.objects.filter(parent__isnull=True).order_by('order').first()
            result = menu.Menu.objects.filter(parent=parent_menu)
        payload = {
            'structure': structure,
            'menu': menu_serializer(result, many=True).data,
        }
        return Response(payload, status=status.HTTP_200_OK)


class VacancyView(CustomModalViewSet):
    # sending vacancy in the company
    queryset = vacancy.Vacancy.objects.all().filter(is_published=True).order_by(
        '-date')
    serializer_class = serializers.VacancySerializer
    pagination_class = None
    http_method_names = ['get']


class StaffView(CustomModalViewSet):
    # sending only leaders in the company
    queryset = ministry.Staff.objects.all().filter(leader=True, is_central=False)
    serializer_class = serializers.StaffSerializer
    pagination_class = None
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        lang = request.headers.get('Accept-Language')
        if lang:
            activate(lang)
        else:
            activate('ru')
        instance = self.get_queryset()
        serializer = self.serializer_class
        staff = serializer(instance, many=True).data
        menu_serializer = StaticMenuSerializer
        page_menu = menu.Menu.objects.filter(url='ministry')
        if page_menu.exists():
            parent_menu = page_menu.first()
            result = menu.Menu.objects.filter(parent=parent_menu)
        else:
            parent_menu = menu.Menu.objects.filter(parent__isnull=True).order_by('order').first()
            result = menu.Menu.objects.filter(parent=parent_menu)
        payload = {
            'staff': staff,
            'menu': menu_serializer(result, many=True).data,
        }
        return Response(payload, status=status.HTTP_200_OK)


class StaffRegionView(CustomModalViewSet):
    queryset = ministry.Staff.objects.all().filter(leader=False, is_central=False, department__isnull=False)
    serializer_class = serializers.StaffRegionalSerializer
    pagination_class = None
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        lang = request.headers.get('Accept-Language')
        if lang:
            activate(lang)
        else:
            activate('ru')
        instance = self.get_queryset()
        serializer = self.serializer_class
        staff = serializer(instance, many=True).data
        menu_serializer = StaticMenuSerializer
        page_menu = menu.Menu.objects.filter(url='ministry')
        if page_menu.exists():
            parent_menu = page_menu.first()
            result = menu.Menu.objects.filter(parent=parent_menu)
        else:
            parent_menu = menu.Menu.objects.filter(parent__isnull=True).order_by('order').first()
            result = menu.Menu.objects.filter(parent=parent_menu)
        payload = {
            'staff': staff,
            'menu': menu_serializer(result, many=True).data,
        }
        return Response(payload, status=status.HTTP_200_OK)


class StaffOrganizationView(CustomModalViewSet):
    queryset = ministry.Staff.objects.all().filter(leader=False, is_central=False, organization__isnull=False)
    serializer_class = serializers.StaffOrganizationSerializer
    pagination_class = None
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        lang = request.headers.get('Accept-Language')
        if lang:
            activate(lang)
        else:
            activate('ru')
        instance = self.get_queryset()
        serializer = self.serializer_class
        staff = serializer(instance, many=True).data
        menu_serializer = StaticMenuSerializer
        page_menu = menu.Menu.objects.filter(url='ministry')
        if page_menu.exists():
            parent_menu = page_menu.first()
            result = menu.Menu.objects.filter(parent=parent_menu)
        else:
            parent_menu = menu.Menu.objects.filter(parent__isnull=True).order_by('order').first()
            result = menu.Menu.objects.filter(parent=parent_menu)
        payload = {
            'staff': staff,
            'menu': menu_serializer(result, many=True).data,
        }
        return Response(payload, status=status.HTTP_200_OK)


class StaffCentralView(CustomModalViewSet):
    queryset = ministry.Staff.objects.all().filter(is_central=True, leader=False)
    serializer_class = serializers.StaffCentralSerializer
    pagination_class = None
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        lang = request.headers.get('Accept-Language')
        if lang:
            activate(lang)
        else:
            activate('ru')
        instance = self.get_queryset()
        serializer = self.serializer_class
        staff = serializer(instance, many=True).data
        menu_serializer = StaticMenuSerializer
        page_menu = menu.Menu.objects.filter(url='ministry')
        if page_menu.exists():
            parent_menu = page_menu.first()
            result = menu.Menu.objects.filter(parent=parent_menu)
        else:
            parent_menu = menu.Menu.objects.filter(parent__isnull=True).order_by('order').first()
            result = menu.Menu.objects.filter(parent=parent_menu)
        payload = {
            'staff': staff,
            'menu': menu_serializer(result, many=True).data,
        }
        return Response(payload, status=status.HTTP_200_OK)


class AllDepartmentView(CustomModalViewSet, generics.ListAPIView):
    queryset = ministry.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    pagination_class = None
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title_uz', 'title_ru', 'title_en', ]
    filterset_fields = ['region']

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        organization_instance = ministry.Organization.objects.all()

        department_serializer = self.serializer_class
        organization_serializer = serializers.OrganizationListSerializer

        context = {
            "request": request,
        }
        department = department_serializer(instance, many=True, context=context)
        organization = organization_serializer(organization_instance, many=True, context=context)

        response = department.data + organization.data
        return Response(response)


class DepartmentView(CustomModalViewSet, generics.ListAPIView):
    """Included both viewset and generic. Search and Filter are not properly supported in viewset only"""
    queryset = ministry.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    pagination_class = None
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title_uz', 'title_ru', 'title_en', ]
    filterset_fields = ['region']

    # def get_queryset(self):
    #     queryset = self.get_queryset()
    #     # Filter: category ID in request params
    #     category = self.request.GET.get('category', None)
    #     if category is not None:
    #         queryset = queryset.filter(category=category)
    #     return queryset


class OrganizationView(DepartmentView):
    queryset = ministry.Organization.objects.all()
    serializer_class = serializers.OrganizationListSerializer
    pagination_class = None
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['region', 'region__title', 'district', 'district__title']

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_class
        else:
            return serializers.OrganizationDetailSerializer


class AdmAboutMinistryView(viewsets.ModelViewSet):
    queryset = ministry.AboutMinistry.objects.all()
    serializer_class = serializers.AdmAboutMinistrySerializer
    pagination_class = None
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]


class AdmMinistryStructureView(viewsets.ModelViewSet):
    queryset = ministry.MinistryStructure.objects.all().order_by('-id')
    serializer_class = serializers.AdmMinistryStructureSerializer
    pagination_class = None
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]


class AdmMinistryStatView(viewsets.ModelViewSet):
    queryset = ministry.MinistryStat.objects.all()
    serializer_class = serializers.AdmMinistryStatSerializer
    pagination_class = None
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]


class AdmMinistryStaffView(viewsets.ModelViewSet):
    queryset = ministry.Staff.objects.all()
    serializer_class = serializers.AdmMinistryStaffSerializer
    pagination_class = pagination.CustomPagination
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        main = self.request.query_params.get('main', None)
        leader = self.request.query_params.get('leader', None)
        department = self.request.query_params.get('department', None)
        organization = self.request.query_params.get('organization', None)
        is_central = self.request.query_params.get('is_central', None)
        params = self.request.query_params.get('params', None)
        q = self.request.query_params.get('q', None)
        filters = {}
        if main:
            filters['main'] = True if main == 'true' else False
        if leader:
            filters['leader'] = True if leader == 'true' else False
        if department:
            filters['department__isnull'] = False
        if organization:
            filters['organization__isnull'] = False
        if is_central:
            filters['is_central'] = True if is_central == 'true' else False
        if params:
            if q and params == 'title':
                filters['title__icontains'] = q
            if q and params == 'position':
                filters['position__icontains'] = q
            if q and params == 'organization':  # organization title
                filters['organization__title__icontains'] = q
        return self.queryset.filter(**filters)


class AdmMinistryDepartmentView(viewsets.ModelViewSet):
    queryset = ministry.Department.objects.all()
    serializer_class = serializers.AdmMinistryDepartmentSerializer
    pagination_class = pagination.CustomPagination
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]
    filterset_fields = ['region']


class AdmMinistryOrganizationView(viewsets.ModelViewSet):
    queryset = ministry.Organization.objects.all()
    serializer_class = serializers.AdmMinistryOrganizationSerializer
    pagination_class = pagination.CustomPagination
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        region = self.request.query_params.get('region', None)
        district = self.request.query_params.get('district', None)
        params = self.request.query_params.get('params', None)
        q = self.request.query_params.get('q', None)
        filters = {}
        if region:
            filters['region__id'] = region
        if district:
            filters['district__id'] = district
        if params:
            if q and params == 'title':
                filters['title__icontains'] = q
            if q and params == 'address':
                filters['address__icontains'] = q
        return self.queryset.filter(**filters)


class VisitorView(viewsets.ModelViewSet):
    queryset = ministry.Visitor.objects.all()
    serializer_class = serializers.VisitorSerializer
    pagination_class = None

    # http_method_names = ['get', 'post', 'put', 'delete']

    def list(self, request, *args, **kwargs):
        try:
            date_from = request.query_params.get('date_from', None)
            date_to = request.query_params.get('date_to', None)
            if date_from and date_to:
                date_from = datetime.strptime(date_from, '%Y-%m-%d')
                date_to = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
                date_from = make_aware(date_from)
                last_week = datetime.now() - timedelta(days=7)
                last_week_visitor_count = ministry.VisitorLog.objects.filter(
                    created_at__range=[last_week, datetime.now()]).count()
                last_month = datetime.now() - timedelta(days=30)
                last_month_visitor_count = ministry.VisitorLog.objects.filter(
                    created_at__range=[last_month, datetime.now()]).count()
                last_year = datetime.now() - timedelta(days=365)
                last_year_visitor_count = ministry.VisitorLog.objects.filter(
                    created_at__range=[last_year, datetime.now()]).count()
                result = ministry.VisitorLog.objects.filter(created_at__range=[date_from, date_to])
                count = result.count()
                return Response({'status': True, 'result_count': count,
                                 'last_week_visitor_count': last_week_visitor_count,
                                 'last_month_visitor_count': last_month_visitor_count,
                                 'last_year_visitor_count': last_year_visitor_count}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'status': False}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            user_agent = request.data['browser']
            ip = request.data['ip']
            if user_agent:
                if_user = self.queryset.filter(browser=user_agent)
                if not if_user:
                    if_user = self.queryset.create(browser=user_agent, ip=ip, device=request.data['device'],
                                                   os=request.data['os'])
                else:
                    if_user = if_user.first()
            current_datetime = datetime.now().date()
            result = ministry.VisitorLog.objects.filter(visitor=if_user, created_at__date=current_datetime)
            if not result:
                ministry.VisitorLog.objects.create(visitor=if_user, url=request.data['ip'])
            count = ministry.VisitorLog.objects.filter(created_at__date=current_datetime).count()
            return Response({'count': count, 'status': True}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'status': False}, status=status.HTTP_400_BAD_REQUEST)


class StaffListView(viewsets.ModelViewSet):
    queryset = ministry.Staff.objects.all()
    serializer_class = serializers.AdmMinistryStaffSerializer
    pagination_class = pagination.CustomPagination
    http_method_names = ['get', ]

    def get_queryset(self):
        main = self.request.query_params.get('main', None)
        leader = self.request.query_params.get('leader', None)
        department = self.request.query_params.get('department', None)
        organization = self.request.query_params.get('organization', None)
        is_central = self.request.query_params.get('is_central', None)
        filters = {}
        if main:
            filters['main'] = True if main == 'true' else False
        if leader:
            filters['leader'] = True if leader == 'true' else False
        if department:
            filters['department__isnull'] = False
        if organization:
            filters['organization__isnull'] = False
        if is_central:
            filters['is_central'] = True if is_central == 'true' else False
        return self.queryset.filter(**filters)  #

    def list(self, request, *args, **kwargs):
        lang = request.headers.get('Accept-Language')
        if lang:
            activate(lang)
        else:
            activate('ru')
        instance = self.get_queryset()
        serializer = self.serializer_class
        staff = serializer(instance, many=True).data
        menu_serializer = StaticMenuSerializer
        page_menu = menu.Menu.objects.filter(url='ministry')
        if page_menu.exists():
            parent_menu = page_menu.first()
            result = menu.Menu.objects.filter(parent=parent_menu)
        else:
            parent_menu = menu.Menu.objects.filter(parent__isnull=True).order_by('order').first()
            result = menu.Menu.objects.filter(parent=parent_menu)
        payload = {
            'staff': staff,
            'menu': menu_serializer(result, many=True).data,
        }
        return Response(payload, status=status.HTTP_200_OK)


class AdmCarsView(viewsets.ModelViewSet):
    queryset = ministry.Cars.objects.all()
    serializer_class = serializers.AdmCarsSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = None
    # http_method_names = ['get', 'post', 'put', 'delete']


class AdmCarInfoView(viewsets.ModelViewSet):
    queryset = ministry.CarInfo.objects.all()
    serializer_class = serializers.AdmCarInfoSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = None
    # http_method_names = ['get', 'post', 'put', 'delete']


class CarInfoView(viewsets.ModelViewSet):
    queryset = ministry.CarInfo.objects.all()
    serializer_class = serializers.CarInfoSerializer
    pagination_class = pagination.CustomPagination
    http_method_names = ['get', ]


class AdmOrganizationTypeView(viewsets.ModelViewSet):
    queryset = ministry.OrganizationType.objects.all()
    serializer_class = serializers.AdmOrganizationTypeSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = None
    # http_method_names = ['get', 'post', 'put', 'delete']


class OrganizationTypeView(viewsets.ModelViewSet):
    queryset = ministry.OrganizationType.objects.all()
    serializer_class = serializers.OrganizationTypeSerializer
    pagination_class = pagination.CustomPagination
    http_method_names = ['get', ]
    lookup_field = 'slug'

    def get_queryset(self):
        if self.request.query_params.get('slug'):
            return self.queryset.filter(slug=self.request.query_params.get('slug'))
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')
        return queryset


class IntegrationErpNumberDataView(viewsets.ModelViewSet):
    queryset = ministry.OrganizationType.objects.all()
    serializer_class = serializers.OrganizationTypeSerializer
    # pagination_class = pagination.CustomPagination
    http_method_names = ['get', ]

    def list(self, request, *args, **kwargs):
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        year = request.query_params.get('year', None)
        # Define the external API URL
        headers = {
            'authority': 'my-api.sport.uz',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,uz;q=0.8,ru;q=0.7',
            'lang_code': 'uz_latn',
            'origin': 'https://my.sport.uz',
            'referer': 'https://my.sport.uz/',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        }
        api_url = 'https://my-api.sport.uz/Helper/GetNumberData'
        # Define the parameters for the GET request
        params = {
            'schoolyearid': 3,
        }
        # Make the GET request to the external API
        response = requests.get(api_url, params=params, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Return the JSON data from the external API
            return Response(response.json())
        else:
            # If the request failed, return an error message
            return Response({'error': 'Failed to retrieve data from the external API'}, status=response.status_code)
