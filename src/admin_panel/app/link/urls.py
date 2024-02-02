from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'link'

urlpatterns = [
    path('', login_required(views.LinkList.as_view()), name='link-list'),
    path('create/', login_required(views.LinkCreate.as_view()), name='link-create'),
    path('update/<int:pk>/', login_required(views.LinkUpdate.as_view()), name='link-update'),
    path('delete/<int:pk>/', login_required(views.LinkDelete.as_view()), name='link-delete'),
]