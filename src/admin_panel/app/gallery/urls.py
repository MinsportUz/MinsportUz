from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views


app_name = 'gallery'

urlpatterns = [
    # Photogallery urls
    path('photo/', login_required(views.PhotoList.as_view()), name='photo-list'),
    path('photo/create/', login_required(views.PhotoCreate.as_view()), name='photo-create'),
    path('photo/update/<int:pk>/', login_required(views.PhotoUpdate.as_view()), name='photo-update'),
    path('photo/delete/<int:pk>/', login_required(views.PhotoDelete.as_view()), name='photo-delete'),

    # Videogallery urls
    path('video/', login_required(views.VideoList.as_view()), name='video-list'),
    path('video/create/', login_required(views.VideoCreate.as_view()), name='video-create'),
    path('video/update/<int:pk>/', login_required(views.VideoUpdate.as_view()), name='video-update'),
    path('video/delete/<int:pk>/', login_required(views.VideoDelete.as_view()), name='video-delete'),

]