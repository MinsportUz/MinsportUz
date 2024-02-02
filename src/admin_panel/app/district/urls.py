from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'district'

urlpatterns = [
    path('', login_required(views.DistrictList.as_view()), name='district-list'),
    path('create/', login_required(views.DistrictCreate.as_view()), name='district-create'),
    path('update/<int:pk>/', login_required(views.DistrictUpdate.as_view()), name='district-update'),
    path('delete/<int:pk>/', login_required(views.DistrictDelete.as_view()), name='district-delete'),

]