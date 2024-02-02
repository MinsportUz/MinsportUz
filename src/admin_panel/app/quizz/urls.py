from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'quizz'

urlpatterns = [
    path('', login_required(views.QuizzList.as_view()), name='quizz-list'),
    path('api/create/', login_required(views.QuizzCreateAPI.as_view()), name='quizz-api-create'),
    path('api/<int:pk>/', login_required(views.QuizzUpdateAPI.as_view()), name='quizz-api-update'),
    path('api/delete/', login_required(views.QuestionDelete.as_view()), name='quizz-api-delete'),
    path('create/', login_required(views.QuizzCreate.as_view()), name='quizz-create'),
    path('update/<int:pk>/', login_required(views.QuizzUpdate.as_view()), name='quizz-update'),
    path('delete/<int:pk>/', login_required(views.QuizzDelete.as_view()), name='quizz-delete'),


]