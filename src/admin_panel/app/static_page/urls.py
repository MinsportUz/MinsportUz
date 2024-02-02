from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'static'

urlpatterns = [
    path('', login_required(views.StaticList.as_view()), name='static-list'),
    path('create/', login_required(views.StaticCreate.as_view()), name='static-create'),
    path('update/<int:pk>/', login_required(views.StaticUpdate.as_view()), name='static-update'),
    path('delete/<int:pk>/', login_required(views.StaticDelete.as_view()), name='static-delete'),
]