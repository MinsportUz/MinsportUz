from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views


app_name = 'vacancy'

urlpatterns = [

    path('', login_required(views.VacancyList.as_view()), name='vacancy-list'),
    path('create/', login_required(views.VacancyCreate.as_view()), name='vacancy-create'),
    path('update/<int:pk>/', login_required(views.VacancyUpdate.as_view()), name='vacancy-update'),
    path('delete/<int:pk>/', login_required(views.VacancyDelete.as_view()), name='vacancy-delete'),

]