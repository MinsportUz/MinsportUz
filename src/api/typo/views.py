from rest_framework import viewsets, generics
from . import serializers


class TypoView(viewsets.ViewSet, generics.CreateAPIView):
    serializer_class = serializers.TypoSerializer
    pagination_class = None
    http_method_names = ['post']
