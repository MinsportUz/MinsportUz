from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('mainpage/', login_required(views.GeneralSettings.as_view()), name='general'),
    # path('create/', login_required(views.TypoCreate.as_view()), name='typo-create'),
    path('contact/', login_required(views.ContactSettings.as_view()), name='contact'),
    # path('delete/<int:pk>/', login_required(views.TypoDelete.as_view()), name='settings-delete'),
]