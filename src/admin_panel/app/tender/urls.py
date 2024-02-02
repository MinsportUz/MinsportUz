from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'tender'

urlpatterns = [
    path('', login_required(views.TenderList.as_view()), name='tender-list'),
    path('create/', login_required(views.TenderCreate.as_view()), name='tender-create'),
    path('update/<int:pk>/', login_required(views.TenderUpdate.as_view()), name='tender-update'),
    path('delete/<int:pk>/', login_required(views.TenderDelete.as_view()), name='tender-delete'),
]