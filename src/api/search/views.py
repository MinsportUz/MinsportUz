from itertools import chain

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, filters
from admin_panel.model import event, press_service, static, question
from . import serializers
from datetime import timedelta, datetime


class Search(APIView):

    # filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # search_fields = [filters.SearchFilter]

    def post(self, request):
        # lang_code = request.LANGUAGE_CODE
        query = self.request.POST.get('query')
        events = event.Event.objects.filter(title__icontains=query)
        quizz = question.Quizz.objects.filter(title__icontains=query)
        news = press_service.News.objects.filter(title__icontains=query)
        photogallery = press_service.PhotoGallery.objects.filter(title__icontains=query)
        videogallery = press_service.VideoGallery.objects.filter(title__icontains=query)
        static_page = static.StaticPage.objects.filter(title__icontains=query)
        # results = chain(events, events, news, photogallery, videogallery, static_page, )

        serializer = serializers.SearchSerializer(
            {'events': events, 'quizz': quizz, 'news': news, 'photogallery': photogallery,
             'videogallery': videogallery, 'static_page': static_page}, context={'request': request})
        return Response(data=serializer.data)


class ImageUploadView(generics.CreateAPIView):
    queryset = press_service.MediaImage.objects.all()
    serializer_class = serializers.MediaImageSerializer
    permission_classes = [IsAuthenticated,]


class SearchWithDate(APIView):

    # filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # search_fields = [filters.SearchFilter]

    def post(self, request):
        # lang_code = request.LANGUAGE_CODE
        date_from = self.request.POST.get('date_from')
        date_to = self.request.POST.get('date_to')
        date_to = (datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
        events = event.Event.objects.filter(created_at__range=[date_from, date_to])
        quizz = question.Quizz.objects.filter(created_at__range=[date_from, date_to])
        news = press_service.News.objects.filter(created_at__range=[date_from, date_to])
        photogallery = press_service.PhotoGallery.objects.filter(created_at__range=[date_from, date_to])
        videogallery = press_service.VideoGallery.objects.filter(created_at__range=[date_from, date_to])
        static_page = static.StaticPage.objects.filter(created_at__range=[date_from, date_to])
        # results = chain(events, events, news, photogallery, videogallery, static_page, )

        serializer = serializers.SearchSerializer(
            {'events': events, 'quizz': quizz, 'news': news, 'photogallery': photogallery,
             'videogallery': videogallery, 'static_page': static_page}, context={'request': request})
        return Response(data=serializer.data)
