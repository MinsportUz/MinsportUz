from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Count, Avg
from admin_panel.model import service
from admin_panel.model.service import EmployeeRating
from rest_framework.decorators import action
from . import serializers
from .. import pagination
from rest_framework.permissions import IsAuthenticated


class CustomModalViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')
        return queryset


class ServiceListView(CustomModalViewSet):
    queryset = service.Service.objects.all()
    serializer_class = serializers.ServiceSerializer
    pagination_class = None
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        more = self.get_queryset().count() > 6
        serializer = self.serializer_class
        payload = {
            'more': more,
            'services': serializer(instance, many=True).data,
        }
        return Response(payload)


class EmployeeRatingModalViewSet(viewsets.ModelViewSet):
    queryset = service.EmployeeRating.objects.all()
    serializer_class = serializers.EmployeeRatingPostSerializer
    pagination_class = pagination.ThirtyPagination
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        page = self.request.query_params.get('page', 1)
        organization_types = self.queryset.values('organization') \
            .annotate(total_count=Count('id'),
                      avg_grade=Avg('grade_type')) \
            .order_by('-total_count', '-avg_grade')
        total_count = len(organization_types)
        organization_types = organization_types[(int(page) - 1) * 30:int(page) * 30]
        organization_summary = []
        counter = (int(page) - 1) * 30 + 1
        for organization in organization_types:
            _organ = service.Organization.objects.get(id=organization['organization'])
            staff = service.Staff.objects.filter(organization=_organ.id).first()
            organization_summary.append({
                'id': counter,
                'region': _organ.region.title,
                'district': _organ.district.title,
                'organization': _organ.title,
                'employee': staff.title if staff else _organ.id,
                'total_count': organization['total_count'],
                'avg_grade': round(organization['avg_grade'], 1)})
            counter += 1
        return Response({
            'page': page,
            'per_page': int(page) - 1 if int(page) > 1 else 1,
            'current_page': int(page),
            'total_pages': int(total_count / 30) + 1 if total_count % 30 != 0 else int(total_count / 30),
            'total': total_count,
            "result": organization_summary})

    @action(detail=False, methods=['get'])
    def summary(self, request):
        service_types = self.queryset.values('service_type') \
                            .annotate(total_count=Count('id'),
                                      avg_grade=Avg('grade_type')) \
                            .order_by('-total_count', '-avg_grade')[:3]
        service_summary = []
        for service in service_types:
            service_name = dict(EmployeeRating.service_choice).get(service['service_type'])
            service_summary.append({'service_type': service_name,
                                    'total_count': service['total_count'],
                                    'avg_grade': round(service['avg_grade'], 1)})
        return Response(service_summary)


class AdmServiceView(viewsets.ModelViewSet):
    queryset = service.Service.objects.all()
    serializer_class = serializers.AdmServiceSerializer
    pagination_class = None
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]