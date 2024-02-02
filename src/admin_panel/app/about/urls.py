from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views

app_name = 'about'

urlpatterns = [
    # path('create/', login_required(views.AboutMinistryCreate.as_view()), name='about-create'),
    path('update/', login_required(views.AboutMinistryUpdate.as_view()), name='about-update'),
    path('structure/update/', login_required(views.MininstryStructureUpdate.as_view()), name='structure-update'),
    path('stat/create/', login_required(views.MinistryStatCreate.as_view()), name='stat-create'),
    path('stat/', login_required(views.MinistryStatList.as_view()), name='stat-list'),
    path('stat/update/<int:pk>/', login_required(views.MinistryStatUpdate.as_view()), name='stat-update'),
    path('stat/delete/<int:pk>/', login_required(views.MinistryStatDelete.as_view()), name='stat-delete'),
    # Department
    path('department/', login_required(views.DepartmentList.as_view()), name='department-list'),
    path('department/create/', login_required(views.DepartmentCreate.as_view()), name='department-create'),
    path('department/update/<int:pk>/', login_required(views.DepartmentUpdate.as_view()), name='department-update'),
    path('department/delete/<int:pk>/', login_required(views.DepartmentDelete.as_view()), name='department-delete'),

    # Organization
    path('organization/', login_required(views.OrganizationList.as_view()), name='organization-list'),
    path('organization/create/', login_required(views.OrganizationCreate.as_view()), name='organization-create'),
    path('organization/update/<int:pk>/', login_required(views.OrganizationUpdate.as_view()), name='organization-update'),
    path('organization/delete/<int:pk>/', login_required(views.OrganizationDelete.as_view()), name='organization-delete'),

    # Staff
    path('staff/', login_required(views.LeaderList.as_view()), name='staff-list'),
    path('staff/department/', login_required(views.LeaderDepartmentList.as_view()), name='staff-department-list'),
    path('staff/organization/', login_required(views.LeaderOrganizationList.as_view()), name='staff-organization-list'),
    path('staff/central/', login_required(views.LeaderCentralList.as_view()), name='staff-central-list'),
    path('staff/create/', login_required(views.LeaderCreate.as_view()), name='staff-create'),
    path('staff/department/create/', login_required(views.LeaderDepartmentCreate.as_view()), name='staff-department-create'),
    path('staff/organization/create/', login_required(views.LeaderOrganizationCreate.as_view()), name='staff-organization-create'),
    path('staff/central/create/', login_required(views.LeaderCentralCreate.as_view()), name='staff-central-create'),

    path('staff/update/<int:pk>/', login_required(views.LeaderUpdate.as_view()), name='staff-update'),
    path('staff/department/update/<int:pk>/', login_required(views.LeaderDepartmentUpdate.as_view()), name='staff-department-update'),
    path('staff/organization/update/<int:pk>/', login_required(views.LeaderOrganizationUpdate.as_view()), name='staff-organization-update'),
    path('staff/central/update/<int:pk>/', login_required(views.LeaderCentralUpdate.as_view()), name='staff-central-update'),

    path('staff/delete/<int:pk>/', login_required(views.LeaderDelete.as_view()), name='staff-delete'),

    path('staff/department/delete/<int:pk>/', login_required(views.StaffDepartmentDelete.as_view()),
         name='staff-department-delete'),
    path('staff/organization/delete/<int:pk>/', login_required(views.StaffOrganizationDelete.as_view()),
         name='staff-organization-delete'),
    path('staff/central/delete/<int:pk>/', login_required(views.StaffCentralDelete.as_view()),
         name='staff-central-delete'),

 
]