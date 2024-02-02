from django.shortcuts import render
from django.utils.timezone import now
from django.views import View

from admin_panel.model import ministry as about, tender, vacancy
from admin_panel.model import press_service as press
from admin_panel.model import docs
from admin_panel.model import static
from admin_panel.model import event

from rolepermissions.decorators import has_role_decorator

from admin_panel.model.user import CustomUser


class Index(View):
    def get(self, request):
        event_count = event.Event.objects.count()
        news_count = press.News.objects.count()
        tender_count = tender.Tender.objects.count()
        vacancy_count = vacancy.Vacancy.objects.count()
        photo_gallery_count = press.PhotoGallery.objects.count()
        video_gallery_count = press.VideoGallery.objects.count()
        media_count = photo_gallery_count + video_gallery_count
        staff_count = about.Staff.objects.count()
        static_page_count = static.StaticPage.objects.count()

        if not request.user.is_superuser:
            custom_user = CustomUser.objects.get(user=request.user)
            latest_news = press.News.objects.filter(region=custom_user.region, is_published=True).order_by(
            '-publish_date')[:5]

            popular_news = press.News.objects.filter(region=custom_user.region, is_published=True).order_by(
            '-views')[:5]
        else:
            latest_news = press.News.objects.all().filter(is_published=True).order_by(
            '-publish_date')[:5]
            popular_news = press.News.objects.filter(is_published=True).order_by(
                '-views')[:5]
        latest_events = event.Event.objects.all().filter(is_published=True).order_by(
            '-event_date')[:5]

        context = {
            'event_count': event_count,
            'news_count': news_count,
            'tender_count': tender_count,
            'media_count': media_count,
            'staff_count': staff_count,
            'vacancy_count': vacancy_count,

            'latest_events': latest_events,
            'latest_news': latest_news,
            'popular_news': popular_news,
            'now': now()
        }
        return render(request, 'back/index.html', context)
