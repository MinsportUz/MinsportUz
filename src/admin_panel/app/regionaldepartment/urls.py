from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'regionaldepartment'

urlpatterns = [


    path('', login_required(views.RegionalDepartmentList.as_view()), name='regionaldepartment-list'),
    path('create/', login_required(views.RegionalDepartmentCreate.as_view()), name='regionaldepartment-create'),
    path('update/<int:pk>/', login_required(views.RegionalDepartmentUpdate.as_view()), name='regionaldepartment-update'),
    path('delete/<int:pk>/', login_required(views.RegionalDepartmentDelete.as_view()), name='regionaldepartment-delete'),
]