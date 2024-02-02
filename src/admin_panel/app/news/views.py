from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView
from rolepermissions.mixins import HasRoleMixin

from django.conf import settings

from admin_panel.app.news import forms
from admin_panel.model import press_service as news, territorial
from admin_panel.app import views as custom
from admin_panel.model.territorial import Region
from admin_panel.model.user import CustomUser
import telebot

tb = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

class NewsCreate(CreateView):
    model = news.News
    form_class = forms.NewsForm
    template_name = 'back/press_service/news/news_create.html'
    success_url = reverse_lazy('news:news-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsCreate, self).get_context_data(object_list=object_list, **kwargs)
        context['news_categories'] = news.NewsCategory.objects.all()
        context['news_smedia'] = news.NewsSMedia.objects.all()
        context['news_hashtags'] = news.NewsHashtag.objects.all()
        context['region'] = territorial.Region.objects.all()
        if not self.request.user.is_superuser:
            context['staff'] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        hashtags = request.POST.getlist('hashtag')

        if data.get('category'):
            data['category'] = news.NewsCategory.objects.get(id=int(data['category']))

        if data.get('hashtag'):
            del data['hashtag']
        if data.get('is_published') == 'on':
            data['is_published'] = True
        else:
            data['is_published'] = False

        if data.get('actual') == 'on':
            data['actual'] = True
        else:
            data['actual'] = False

        if data.get('main_page') == 'on':
            data['main_page'] = True
        else:
            data['main_page'] = False

        if not data['publish_date']:
            del data['publish_date']

        if not data.get('region') == '':
            data['region'] = Region.objects.get(id=int(data['region']))
        else:
            del data['region']

        # obj = self.model(**data)
        obj = self.model.objects.create(**data)

        thumbnail = request.FILES.get('thumbnail')
        if thumbnail:
            obj.thumbnail = thumbnail
            obj.cover = thumbnail

        image = request.FILES.get('image')
        if image:
            obj.image = image

        if request.LANGUAGE_CODE == 'en':
            for hashtag in hashtags:
                if news.NewsHashtag.objects.filter(title_en=hashtag).exists():
                    tag = news.NewsHashtag.objects.get(title_en=hashtag)
                else:
                    tag = news.NewsHashtag.objects.create(title_en=hashtag)

                obj.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == 'ru':
            for hashtag in hashtags:
                if news.NewsHashtag.objects.filter(title_ru=hashtag).exists():
                    tag = news.NewsHashtag.objects.get(title_ru=hashtag)
                else:
                    tag = news.NewsHashtag.objects.create(title_ru=hashtag)

                obj.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == 'uz':
            for hashtag in hashtags:
                if news.NewsHashtag.objects.filter(title_uz=hashtag).exists():
                    tag = news.NewsHashtag.objects.get(title_uz=hashtag)
                else:
                    tag = news.NewsHashtag.objects.create(title_uz=hashtag)

                obj.hashtag.add(tag.id)

        obj.save()
        return HttpResponseRedirect(self.success_url)


class NewsUpdate(UpdateView):
    model = news.News
    form_class = forms.NewsForm
    context_object_name = 'news'
    template_name = 'back/press_service/news/news_update.html'
    success_url = reverse_lazy('news:news-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context['news_categories'] = news.NewsCategory.objects.all()
        context['news_hashtags'] = news.NewsHashtag.objects.all()
        context['region'] = territorial.Region.objects.all()
        if not self.request.user.is_superuser:
            context['staff'] = CustomUser.objects.get(user=self.request.user)

        return context

    def get(self, request, *args, **kwargs):
        obj = news.News.objects.filter(id=self.kwargs['pk'])
        if not self.request.user.is_superuser:
            staff = CustomUser.objects.get(user=self.request.user)
            if obj.exists():
                if not staff.region == obj.last().region:
                    return HttpResponseRedirect(self.success_url)
        return super(NewsUpdate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        hashtags = request.POST.getlist('hashtag')
        if data.get('category'):
            data['category'] = news.NewsCategory.objects.get(id=int(data['category']))

        if data.get('hashtag'):
            del data['hashtag']
        if data.get('is_published') == 'on':
            data['is_published'] = True
        else:
            data['is_published'] = False

        if data.get('actual') == 'on':
            data['actual'] = True
        else:
            data['actual'] = False

        if data.get('main_page') == 'on':
            data['main_page'] = True
        else:
            data['main_page'] = False

        if not data['publish_date']:
            del data['publish_date']

        if not data.get('region') == '':
            data['region'] = Region.objects.get(id=int(data['region']))
        else:
            del data['region']

        obj = self.model.objects.get(id=self.kwargs['pk'])
        obj.category = data['category']
        obj.region = data.get('region')

        obj.title_uz = data.get('title_uz')
        obj.title_ru = data.get('title_ru')
        obj.title_en = data.get('title_en')

        obj.description_uz = data.get('description_uz')
        obj.description_ru = data.get('description_ru')
        obj.description_en = data.get('description_en')

        obj.short_description_uz = data.get('short_description_uz')
        obj.short_description_ru = data.get('short_description_ru')
        obj.short_description_en = data.get('short_description_en')

        obj.publish_date = data.get('publish_date')
        obj.is_published = data.get('is_published')
        obj.actual = data.get('actual')
        obj.main_page = data.get('main_page')

        thumbnail = request.FILES.get('thumbnail')
        if thumbnail:
            obj.thumbnail = thumbnail
            obj.cover = thumbnail

        image = request.FILES.get('image')
        if image:
            obj.image = image

        obj.video_link = data.get('video_link')

        for i in obj.hashtag.all():
            obj.hashtag.remove(i)

        if request.LANGUAGE_CODE == 'en':
            for hashtag in hashtags:
                if news.NewsHashtag.objects.filter(title_en=hashtag).exists():
                    tag = news.NewsHashtag.objects.get(title_en=hashtag)
                else:
                    tag = news.NewsHashtag.objects.create(title_en=hashtag)
                if tag not in obj.hashtag.all():
                    obj.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == 'ru':
            for hashtag in hashtags:
                if news.NewsHashtag.objects.filter(title_ru=hashtag).exists():
                    tag = news.NewsHashtag.objects.get(title_ru=hashtag)
                else:
                    tag = news.NewsHashtag.objects.create(title_ru=hashtag)
                if tag not in obj.hashtag.all():
                    obj.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == 'uz':
            for hashtag in hashtags:
                if news.NewsHashtag.objects.filter(title_uz=hashtag).exists():
                    tag = news.NewsHashtag.objects.get(title_uz=hashtag)
                else:
                    tag = news.NewsHashtag.objects.create(title_uz=hashtag)
                if obj not in obj.hashtag.all():
                    obj.hashtag.add(tag.id)

        obj.save()
        return HttpResponseRedirect(self.success_url)


class NewsList(custom.CustomListView):
    model = news.News
    template_name = 'back/press_service/news/news_list.html'
    queryset = model.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsList, self).get_context_data(object_list=object_list)
        objects = self.queryset
        if not self.request.user.is_superuser:
            user = CustomUser.objects.get(user=self.request.user)
            objects = self.queryset.filter(region=user.region)

        q = self.request.GET.get('q')
        if q:
            if self.request.LANGUAGE_CODE == 'en':
                objects = self.model.objects.filter(title_en__icontains=q)
            if self.request.LANGUAGE_CODE == 'ru':
                objects = self.model.objects.filter(title_ru__icontains=q)
            if self.request.LANGUAGE_CODE == 'uz':
                objects = self.model.objects.filter(title_uz__icontains=q)

        page = self.request.GET.get('page', 1)
        paginator = Paginator(objects, 12)

        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)

        context['objects'] = objects
        return context


class NewsDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.News
    success_url = reverse_lazy('news:news-list')


class NewsCategoryCreate(HasRoleMixin, custom.CustomCreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.NewsCategory
    form_class = forms.NewsCategoryForm
    template_name = 'back/press_service/news/news_category_create.html'
    success_url = reverse_lazy('news:category-list')


class NewsCategoryUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.NewsCategory
    form_class = forms.NewsCategoryForm
    context_object_name = 'object'
    template_name = 'back/press_service/news/news_category_update.html'
    success_url = reverse_lazy('news:category-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        obj = self.model.objects.get(id=self.kwargs['pk'])
        obj.title_uz = data['title_uz']
        obj.title_ru = data['title_ru']
        obj.title_en = data['title_en']
        obj.order = data['order']

        obj.save()
        return HttpResponseRedirect(self.success_url)


class NewsCategoryList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.NewsCategory
    template_name = 'back/press_service/news/news_category_list.html'
    queryset = model.objects.all()


class NewsCategoryDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.NewsCategory
    success_url = reverse_lazy('news:category-list')


class NewsHashtagCreate(HasRoleMixin, custom.CustomCreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.NewsHashtag
    form_class = forms.NewsHashtagForm
    template_name = 'back/press_service/news/news_hashtag_create.html'
    success_url = reverse_lazy('news:hashtag-list')


class NewsHashtagUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.NewsHashtag
    form_class = forms.NewsHashtagForm
    context_object_name = 'object'
    template_name = 'back/press_service/news/news_hashtag_update.html'
    success_url = reverse_lazy('news:hashtag-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        obj = self.model.objects.get(id=self.kwargs['pk'])

        obj.title_uz = data['title_uz']
        obj.title_ru = data['title_ru']
        obj.title_en = data['title_en']

        obj.save()
        return HttpResponseRedirect(self.success_url)


class NewsHashtagList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.NewsHashtag
    template_name = 'back/press_service/news/news_hashtag_list.html'
    queryset = model.objects.all()


class NewsHashtagDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.NewsHashtag
    success_url = reverse_lazy('news:hashtag-list')


# FAQ

class FAQCreate(HasRoleMixin, custom.CustomCreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.FAQ
    template_name = 'back/press_service/faq/create.html'
    form_class = forms.FAQForm
    success_url = reverse_lazy('news:faq-list')


class FAQUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.FAQ
    template_name = 'back/press_service/faq/update.html'
    form_class = forms.FAQForm
    context_object_name = 'object'
    success_url = reverse_lazy('news:faq-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        obj = self.model.objects.get(id=self.kwargs['pk'])

        obj.title_uz = data['title_uz']
        obj.title_ru = data['title_ru']
        obj.title_en = data['title_en']

        obj.description_uz = data['description_uz']
        obj.description_ru = data['description_ru']
        obj.description_en = data['description_en']

        obj.order = data['order']

        obj.save()
        return HttpResponseRedirect(self.success_url)


class FAQList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.FAQ
    template_name = 'back/press_service/faq/list.html'
    queryset = model.objects.all()


class FAQDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.FAQ
    success_url = reverse_lazy('news:faq-list')


# PRESS
class PressCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.Press
    template_name = 'back/press_service/press/press_create.html'
    form_class = forms.PressForm
    success_url = reverse_lazy('news:press-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        obj = self.model.objects.create(**data)
        icon = request.FILES.get('icon')
        if icon:
            obj.icon = icon

        obj.save()
        return HttpResponseRedirect(self.success_url)


class PressUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.Press
    template_name = 'back/press_service/press/press_update.html'
    form_class = forms.PressForm
    success_url = reverse_lazy('news:press-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        obj = self.model.objects.get(id=self.kwargs['pk'])

        obj.title = data['title']
        obj.link = data['link']
        icon = request.FILES.get('icon')
        if icon:
            obj.icon = icon

        obj.save()
        return HttpResponseRedirect(self.success_url)


class PressList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.Press
    template_name = 'back/press_service/press/press_list.html'
    queryset = model.objects.all()


class PressDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.Press
    success_url = reverse_lazy('news:press-list')


# ARTICLE
class ArticleCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.PressArticleLink
    template_name = 'back/press_service/press/article_create.html'
    form_class = forms.ArticleForm
    success_url = reverse_lazy('news:article-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleCreate, self).get_context_data(object_list=object_list, **kwargs)
        context['press'] = news.Press.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        data['press'] = news.Press.objects.get(id=int(data['press']))
        if data['is_published'] == 'on':
            data['is_published'] = True
        else:
            data['is_published'] = False

        if not data['publish_date']:
            del data['publish_date']

        obj = self.model.objects.create(**data)

        obj.save()
        return HttpResponseRedirect(self.success_url)


class ArticleUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.PressArticleLink
    template_name = 'back/press_service/press/article_update.html'
    form_class = forms.ArticleForm
    context_object_name = 'object'
    success_url = reverse_lazy('news:article-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context['press'] = news.Press.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        data['press'] = news.Press.objects.get(id=int(data['press']))
        if data.get('is_published') == 'on':
            data['is_published'] = True
        else:
            data['is_published'] = False

        if not data['publish_date']:
            del data['publish_date']

        obj = self.model.objects.get(id=self.kwargs['pk'])

        obj.title = data['title']
        obj.link = data['link']
        obj.language = data['language']
        obj.press = data['press']
        obj.is_published = data['is_published']
        obj.publish_date = data.get('publish_date')

        obj.save()
        return HttpResponseRedirect(self.success_url)


class ArticleList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.PressArticleLink
    template_name = 'back/press_service/press/article_list.html'
    queryset = model.objects.all()


class ArticleDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = news.PressArticleLink
    success_url = reverse_lazy('news:article-list')


# NEWS MEDIA 
class NewsMedia(UpdateView):
    model = news.NewsSMedia
    form_class = forms.NewsForm
    context_object_name = 'news'
    template_name = 'back/press_service/news/news_list.html'
    success_url = reverse_lazy('news:news-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsMedia, self).get_context_data(object_list=object_list, **kwargs)
        context['news_categories'] = news.NewsCategory.objects.all()
        context['news_hashtags'] = news.NewsHashtag.objects.all()
        context['region'] = territorial.Region.objects.all()
        if not self.request.user.is_superuser:
            context['staff'] = CustomUser.objects.get(user=self.request.user)

        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        recent_news = news.News.objects.get(id=self.kwargs['pk'])

        if self.model.objects.filter(news=self.kwargs['pk']).exists():
            #IF exist table in newsmedia
            obj = self.model.objects.get(news=self.kwargs['pk'])

            if data.get('telegram'):
                #send to telegram
                tb.send_photo(settings.CHANNEL_ID, recent_news.cover ,caption="<b>"+recent_news.title_uz+"</b>\n\nБатафсил: https://minsport.uz/uz/news/post/"+str(recent_news.id)+"\n\n<a href='https://t.me/Minsportuz'>Telegram</a> <a href='https://bit.ly/30pICdW'>|</a> <a href='https://www.instagram.com/minsportuz/'>Instagram</a> <a href='https://bit.ly/30pICdW'>|</a> <a href='https://bit.ly/30pICdW'>YouTube</a> <a href='https://m.facebook.com/story.php?story_fbid=573668693557367&id=100027427240464'>|</a> <a href='https://m.facebook.com/story.php?story_fbid=573668693557367&id=100027427240464'>Facebook</a>", parse_mode="HTML")

                obj.telegram = True
            if data.get('facebook'):
                obj.facebook = True

            obj.save()
        else:
             #IF not exist table in newsmedia
            if data.get('telegram'):
                #send to telegram
                tb.send_photo(settings.CHANNEL_ID, recent_news.cover ,caption="<b>"+recent_news.title_uz+"</b>\n\nБатафсил: https://minsport.uz/uz/news/post/"+str(recent_news.id)+"\n\n<a href='https://t.me/Minsportuz'>Telegram</a> <a href='https://bit.ly/30pICdW'>|</a> <a href='https://www.instagram.com/minsportuz/'>Instagram</a> <a href='https://bit.ly/30pICdW'>|</a> <a href='https://bit.ly/30pICdW'>YouTube</a> <a href='https://m.facebook.com/story.php?story_fbid=573668693557367&id=100027427240464'>|</a> <a href='https://m.facebook.com/story.php?story_fbid=573668693557367&id=100027427240464'>Facebook</a>", parse_mode="HTML")
                data['telegram'] = True
                data['facebook'] = False
            if data.get('facebook'):
                data['facebook'] = True
                data['telegram'] = False
            data['news'] = news.News.objects.get(id=int(self.kwargs['pk']))
            obj = self.model.objects.create(**data)


        return HttpResponseRedirect(self.success_url)


# # IMAGE UPLOAD
# class ImageUpload(CreateView):
#     model = news.MediaImage
#     form_class = forms.ImageUploadForm
#     # template_name = 'back/press_service/news/news_create.html'
#     success_url = reverse_lazy('news:news-list')
#
#     def form_valid(self, form):
#         image = form.save(commit=False)
#
#         # I do other stuff here
#         image.save()
#         return JsonResponse({'data': image.image_url})

        # return HttpResponseRedirect(self.success_url)
