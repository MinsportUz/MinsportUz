from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'typo'

urlpatterns = [
    path('', login_required(views.TypoList.as_view()), name='typo-list'),
    # path('create/', login_required(views.TypoCreate.as_view()), name='typo-create'),
    path('update/<int:pk>/', login_required(views.TypoUpdate.as_view()), name='typo-update'),
    path('delete/<int:pk>/', login_required(views.TypoDelete.as_view()), name='typo-delete'),
]