from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'docs'

urlpatterns = [
    path('', login_required(views.DocsList.as_view()), name='docs-list'),
    path('create/', login_required(views.DocsCreate.as_view()), name='docs-create'),
    path('update/<int:pk>/', login_required(views.DocsUpdate.as_view()), name='docs-update'),
    path('delete/<int:pk>/', login_required(views.DocsDelete.as_view()), name='docs-delete'),

    path('type/', login_required(views.DocTypeList.as_view()), name='doc-type-list'),
    path('type/create/', login_required(views.DocTypeCreate.as_view()), name='doc-type-create'),
    path('type/update/<int:pk>/', login_required(views.DocTypeUpdate.as_view()), name='doc-type-update'),
    path('type/delete/<int:pk>/', login_required(views.DocTypeDelete.as_view()), name='doc-type-delete'),


]