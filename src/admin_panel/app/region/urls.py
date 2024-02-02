from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'region'

urlpatterns = [
    path('', login_required(views.RegionList.as_view()), name='region-list'),
    path('create/', login_required(views.RegionCreate.as_view()), name='region-create'),
    path('update/<int:pk>/', login_required(views.RegionUpdate.as_view()), name='region-update'),
    path('delete/<int:pk>/', login_required(views.RegionDelete.as_view()), name='region-delete'),


]