from django.utils.timezone import now
from rest_framework import viewsets, status
from rest_framework.response import Response
from . import serializers
from api.news import serializers as news_serializers
from admin_panel.model import ministry as about, tender, vacancy
from admin_panel.model import press_service as press
from admin_panel.model import event
from admin_panel.model.user import CustomUser, User
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class AdmEventListSerializer(serializers.serializers.ModelSerializer):
    class Meta:
        model = event.Event
        fields = '__all__'


class IndexView(viewsets.ModelViewSet):
    queryset = about.AboutMinistry.objects.all()
    serializer_class = serializers.SettingsSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        event_count = event.Event.objects.count()
        news_count = press.News.objects.count()
        tender_count = tender.Tender.objects.count()
        vacancy_count = vacancy.Vacancy.objects.count()
        photo_gallery_count = press.PhotoGallery.objects.count()
        video_gallery_count = press.VideoGallery.objects.count()
        media_count = photo_gallery_count + video_gallery_count
        staff_count = about.Staff.objects.count()

        if not request.user.is_superuser:
            try:
                custom_user = CustomUser.objects.get(user=request.user)
                # Ensure custom_user is not None before accessing its attributes
                latest_news = press.News.objects.filter(region=custom_user.region, is_published=True).order_by(
                    '-publish_date')[:5]
                popular_news = press.News.objects.filter(region=custom_user.region, is_published=True).order_by(
                    '-views')[:5]
            except Exception:
                # Handle the case where custom_user is not found
                latest_news = press.News.objects.all().filter(is_published=True).order_by(
                    '-publish_date')[:5]
                popular_news = press.News.objects.filter(is_published=True).order_by(
                    '-views')[:5]
        else:
            latest_news = press.News.objects.all().filter(is_published=True).order_by(
                '-publish_date')[:5]
            popular_news = press.News.objects.filter(is_published=True).order_by(
                '-views')[:5]
        # latest_events = event.Event.objects.all().filter(is_published=True).order_by(
        #     '-event_date')[:5]

        context = {
            'event_count': event_count,
            'news_count': news_count,
            'tender_count': tender_count,
            'media_count': media_count,
            'staff_count': staff_count,
            'vacancy_count': vacancy_count,
            # 'latest_events': AdmEventListSerializer(latest_events).data,
            'latest_events' : [],
            'latest_news': news_serializers.NewsListSerializer(latest_news, many=True).data,
            'popular_news': news_serializers.NewsListSerializer(popular_news, many=True).data,
            'now': now()
        }
        return Response(context, status=status.HTTP_200_OK)
