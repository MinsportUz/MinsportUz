from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'menu'

urlpatterns = [
    # Some methods used API calls
    path('api/', login_required(views.MenuCreateAPIView.as_view()), name='menu-api'),
    path('api/create/', login_required(views.MenuCreateAPI.as_view()), name='menu-create-api'),
    path('api/delete/', login_required(views.MenuDeleteAPI.as_view()), name='menu-deletes-api'),
    path('', login_required(views.MenuCreate.as_view()), name='menu-create'),
    # path('create/', login_required(views.MenuCreate.as_view()), name='menu-create'),
    # path('update/<int:pk>/', login_required(views.MenuUpdate.as_view()), name='menu-update'),
    # path('delete/<int:pk>/', login_required(views.MenuDelete.as_view()), name='menu-delete'),
]