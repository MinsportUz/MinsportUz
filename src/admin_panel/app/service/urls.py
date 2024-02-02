from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views

app_name = 'service'

urlpatterns = [
    path('', login_required(views.ServiceList.as_view()), name='service-list'),
    path('create/', login_required(views.ServiceCreate.as_view()), name='service-create'),
    path('update/<int:pk>/', login_required(views.ServiceUpdate.as_view()), name='service-update'),
    path('delete/<int:pk>/', login_required(views.ServiceDelete.as_view()), name='service-delete'),
]