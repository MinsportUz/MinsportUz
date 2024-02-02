from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views

app_name = 'news'

urlpatterns = [
    path('', login_required(views.NewsList.as_view()), name='news-list'),
    path('create/', login_required(views.NewsCreate.as_view()), name='news-create'),

    path('media/<int:pk>/', login_required(views.NewsMedia.as_view()), name='news-media'),

    path('update/<int:pk>/', login_required(views.NewsUpdate.as_view()), name='news-update'),
    path('delete/<int:pk>/', login_required(views.NewsDelete.as_view()), name='news-delete'),

    path('category/', login_required(views.NewsCategoryList.as_view()), name='category-list'),
    path('category/create/', login_required(views.NewsCategoryCreate.as_view()), name='category-create'),
    path('category/update/<int:pk>/', login_required(views.NewsCategoryUpdate.as_view()), name='category-update'),
    path('category/delete/<int:pk>/', login_required(views.NewsCategoryDelete.as_view()), name='category-delete'),

    path('hashtag/', login_required(views.NewsHashtagList.as_view()), name='hashtag-list'),
    path('hashtag/create/', login_required(views.NewsHashtagCreate.as_view()), name='hashtag-create'),
    path('hashtag/update/<int:pk>/', login_required(views.NewsHashtagUpdate.as_view()), name='hashtag-update'),
    path('hashtag/delete/<int:pk>/', login_required(views.NewsHashtagDelete.as_view()), name='hashtag-delete'),


    path('faq/', login_required(views.FAQList.as_view()), name='faq-list'),
    path('faq/create/', login_required(views.FAQCreate.as_view()), name='faq-create'),
    path('faq/update/<int:pk>/', login_required(views.FAQUpdate.as_view()), name='faq-update'),
    path('faq/delete/<int:pk>/', login_required(views.FAQDelete.as_view()), name='faq-delete'),

    path('press/', login_required(views.PressList.as_view()), name='press-list'),
    path('press/create/', login_required(views.PressCreate.as_view()), name='press-create'),
    path('press/update/<int:pk>/', login_required(views.PressUpdate.as_view()), name='press-update'),
    path('press/delete/<int:pk>/', login_required(views.PressDelete.as_view()), name='press-delete'),


    path('article/', login_required(views.ArticleList.as_view()), name='article-list'),
    path('article/create/', login_required(views.ArticleCreate.as_view()), name='article-create'),
    path('article/update/<int:pk>/', login_required(views.ArticleUpdate.as_view()), name='article-update'),
    path('article/delete/<int:pk>/', login_required(views.ArticleDelete.as_view()), name='article-delete'),


]
