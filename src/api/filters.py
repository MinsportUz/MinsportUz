# from rest_framework.filters import BaseFilterBackend
#
#
# class CategoryFilter(BaseFilterBackend):
#     """
#     Filter that only allows users to see their own objects.
#     """
#     def filter_queryset(self, request, queryset, view):
#         param = request.QUERY_PARAMS.get('category', None)
#         if param is not None:
#             return queryset.filter(category=param)
#         return queryset
# import django_filters
from django_filters import filters

from admin_panel.model import event
from rest_framework import filters as rs_filters
from django.utils.translation import get_language
from django.db.models import Q


class CustomDateFilter(filters.Filter):
    date_time = django_filters.DateTimeFilter(name="date_time", lookup_expr='gte')


class NewsHashtagFilter(rs_filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        search = request.query_params.get('title', None)
        if search is None:
            return queryset
        queryset = queryset.filter(
            Q(title_uz__icontains=search) | Q(title_ru__icontains=search) | Q(title_en__icontains=search))
        return queryset
