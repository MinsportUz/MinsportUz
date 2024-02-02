from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import Now

from . import serializers
from api import pagination
from admin_panel.model import press_service
from api.filters import NewsHashtagFilter


class CustomModalViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')

        return queryset


class NewsListView(CustomModalViewSet, generics.ListAPIView):
    """
    The model will be parent for the remaining secondary news class
    Its parameters will be used & inherited

    2. Include generics to use filters&search in params
    """
    queryset = press_service.News.objects.filter(is_published=True, publish_date__lte=Now()).exclude(
        title__exact='').order_by('-publish_date')
    pagination_class = pagination.MidShort
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', 'category__slug', 'hashtag__slug', 'region__slug']
    search_fields = ['title_uz', 'title_ru', 'title_en', ]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.NewsDetailSerializer
        return serializers.NewsListSerializer


    def retrieve(self, request, *args, **kwargs):
        # customization here
        instance = self.get_object()
        instance.views += 1
        instance.save()
        url = reverse('news-api-detail', args=(instance.id,), request=request)
        related = self.get_queryset().filter(category=instance.category, publish_date__lte=Now()).exclude(
            id=instance.id, )[:4]
        related_serializer = serializers.NewsListSerializer

        payload = {
            'news': self.get_serializer(instance).data,
            'url': url,
            'related': related_serializer(related, many=True).data
        }
        return Response(payload)


class IndexNewsListView(NewsListView):
    """
    News list for Web Index
    """
    queryset = press_service.News.objects.filter(is_published=True, main_page=True, publish_date__lte=Now()).order_by(
        '-publish_date')

    pagination_class = None

    def list(self, request, *args, **kwargs):
        top = self.get_queryset().first()
        instance = self.get_queryset()[:8]
        top_serializer = serializers.NewsTopSerializer
        payload = {
            'top': top_serializer(top).data,
            # 'news': serializer(instance, many=True).data,
            'news': top_serializer(instance, many=True).data,
        }
        return Response(payload)


class HeaderNewsListView(NewsListView):
    pagination_class = None
    queryset = press_service.News.objects.filter(is_published=True, publish_date__lte=Now()).order_by('-publish_date')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.NewsDetailSerializer
        return serializers.HeaderNewsSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()[:20]
        serializer = self.get_serializer_class()
        return Response(serializer(queryset, many=True).data)


class IndexNewsLongListView(IndexNewsListView):
    """
    News list for Mobile Index
    """

    def list(self, request, *args, **kwargs):
        top = self.get_queryset().first()
        instance = self.get_queryset().exclude(id=top.id)[:6]
        serializer = serializers.NewsListSerializer
        payload = {
            'top': serializer(top).data,
            'news': serializer(instance, many=True).data,
        }
        return Response(payload)


class MainNewsListView(viewsets.ModelViewSet, generics.ListAPIView):
    """ Inherited from NewsList class. The function will be overrided here"""
    queryset = press_service.News.objects.filter(is_published=True, publish_date__lte=Now()).order_by('-publish_date')
    pagination_class = None
    http_method_names = ['get']
    serializer_class = serializers.NewsListSerializer

    def get_queryset(self):
        param = self.request.query_params.get('category__slug')
        queryset = self.queryset.exclude(title__exact='')[:8]
        if param is not None:
            queryset = self.queryset.filter(category__slug=param).exclude(title__exact='')[:8]
        return queryset


class NewsRegionView(NewsListView):
    queryset = press_service.News.objects.filter(is_published=True, region__isnull=False,
                                                 publish_date__lte=Now()).order_by('-publish_date')
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['region__slug']


class NewsCategoryView(CustomModalViewSet):
    queryset = press_service.NewsCategory.objects.all()
    serializer_class = serializers.NewsCategoryserializer
    http_method_names = ['get']
    pagination_class = None


class NewsHashtagView(CustomModalViewSet):
    queryset = press_service.NewsHashtag.objects.all()
    serializer_class = serializers.NewsHashtagserializer
    http_method_names = ['get']
    pagination_class = None


class PressListView(CustomModalViewSet):
    queryset = press_service.PressArticleLink.objects.filter(is_published=True, publish_date__lte=Now()).order_by(
        '-publish_date')
    serializer_class = serializers.PressSerializer
    pagination_class = None
    http_method_names = ['get']


class FAQListView(CustomModalViewSet):
    queryset = press_service.FAQ.objects.all()
    serializer_class = serializers.FAQSerializer
    pagination_class = None
    http_method_names = ['get']


class NewsIntegration(CustomModalViewSet):
    queryset = press_service.News.objects.all()
    serializer_class = serializers.NewsIntegration
    pagination_class = pagination.NewsPagination
    http_method_names = ['get']

    def get_queryset(self):
        queryset = super().get_queryset()
        from_datetime = self.request.query_params.get('from_datetime')
        to_datetime = self.request.query_params.get('to_datetime')

        if from_datetime and to_datetime:
            queryset = queryset.filter(
                Q(publish_date__gte=from_datetime) &
                Q(publish_date__lte=to_datetime)
            )
        elif from_datetime:
            queryset = queryset.filter(publish_date__gte=from_datetime)
        elif to_datetime:
            queryset = queryset.filter(publish_date__lte=to_datetime)

        return queryset


class AdmNewsView(viewsets.ModelViewSet):
    queryset = press_service.News.objects.all().order_by('-id')
    serializer_class = serializers.AdmNewsSerializer
    pagination_class = pagination.DoubleShort
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated,]
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['title',]

    # def create(self, request, *args, **kwargs):
    #     hashtag = request.data.get('hashtag')
    #     if hashtag:
    #         hashtag = [int(h) for h in hashtag.split(',')]
    #         request.data['hashtag'] = hashtag
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'message': 'Successfully created'}, status=201)
    #     return Response(serializer.errors, status=400)


class AdmNewsSMediaView(viewsets.ModelViewSet):
    queryset = press_service.NewsSMedia.objects.all()
    serializer_class = serializers.AdmNewsSMediaSerializer
    pagination_class = pagination.NewsPagination
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated,]

    def create(self, request, *args, **kwargs):
        news_id = request.data.get('news')
        news_media = self.queryset.filter(news=news_id)
        if news_media:
            news_media_ = news_media.first()
            if request.data.get('facebook'):
                news_media_.facebook = request.data.get('facebook')
            if request.data.get('telegram'):
                news_media_.telegram = request.data.get('telegram')
            news_media_.save()
            return Response({'message': 'Successfully updated'}, status=200)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Successfully created'}, status=201)
        return Response(serializer.errors, status=400)


class AdmMediaImageView(viewsets.ModelViewSet):
    queryset = press_service.MediaImage.objects.all()
    serializer_class = serializers.AdmMediaImageSerializer
    pagination_class = pagination.NewsPagination
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated,]


class AdmNewsHashtagView(viewsets.ModelViewSet):
    queryset = press_service.NewsHashtag.objects.all()
    serializer_class = serializers.AdmNewsHashtagSerializer
    pagination_class = pagination.NewsPagination
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated,]


class AdmNewsCategoryView(viewsets.ModelViewSet):
    queryset = press_service.NewsCategory.objects.all()
    serializer_class = serializers.AdmNewsCategorySerializer
    pagination_class = None
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated,]


class AdmPhotoGalleryView(viewsets.ModelViewSet):
    queryset = press_service.PhotoGallery.objects.all()
    serializer_class = serializers.AdmPhotoGallerySerializer
    pagination_class = None
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated,]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        press_service.PhotoGalleryImage.objects.filter(photo_gallery=instance).delete()
        return super().update(request, *args, **kwargs)


class AdmPhotoGalleryImageView(viewsets.ModelViewSet):
    queryset = press_service.PhotoGalleryImage.objects.all()
    serializer_class = serializers.AdmPhotoGalleryImageSerializer
    pagination_class = None
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated,]


class AdmVideoGalleryView(viewsets.ModelViewSet):
    queryset = press_service.VideoGallery.objects.all()
    serializer_class = serializers.AdmVideoGallerySerializer
    pagination_class = None
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated,]


class AdmPressView(viewsets.ModelViewSet):
    queryset = press_service.Press.objects.all()
    serializer_class = serializers.AdmPressSerializer
    pagination_class = None
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated,]


class AdmPressArticleLinkView(viewsets.ModelViewSet):
    queryset = press_service.PressArticleLink.objects.all()
    serializer_class = serializers.AdmPressArticleLinkSerializer
    pagination_class = None
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated,]


class AdmFAQView(viewsets.ModelViewSet):
    queryset = press_service.FAQ.objects.all()
    serializer_class = serializers.AdmFAQSerializer
    pagination_class = None
    # http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated,]


class NewsHashtagSearchView(viewsets.ModelViewSet):
    queryset = press_service.NewsHashtag.objects.all()
    serializer_class = serializers.NewsHashtagserializer
    http_method_names = ['get']
    pagination_class = pagination.NewsPagination
    filter_backends = [NewsHashtagFilter, ]
    search_fields = ['title', ]
    # permission_classes = [IsAuthenticated,]