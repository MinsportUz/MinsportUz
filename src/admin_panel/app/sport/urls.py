from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'sport'

urlpatterns = [
    path('type/', login_required(views.TypeList.as_view()), name='type-list'),
    path('type/create/', login_required(views.TypeCreate.as_view()), name='type-create'),
    path('type/update/<int:pk>/', login_required(views.TypeUpdate.as_view()), name='type-update'),
    path('type/delete/<int:pk>/', login_required(views.TypeDelete.as_view()), name='type-delete'),

    path('stadion/', login_required(views.StadionList.as_view()), name='stadion-list'),
    path('stadion/create/', login_required(views.StadionCreate.as_view()), name='stadion-create'),
    path('stadion/update/<int:pk>/', login_required(views.StadionUpdate.as_view()), name='stadion-update'),
    path('stadion/delete/<int:pk>/', login_required(views.StadionDelete.as_view()), name='stadion-delete'),

    path('champion/', login_required(views.ChampionList.as_view()), name='champion-list'),
    path('champion/create/', login_required(views.ChampionCreate.as_view()), name='champion-create'),
    path('champion/update/<int:pk>/', login_required(views.ChampionUpdate.as_view()), name='champion-update'),
    path('champion/delete/<int:pk>/', login_required(views.ChampionDelete.as_view()), name='champion-delete'),



]