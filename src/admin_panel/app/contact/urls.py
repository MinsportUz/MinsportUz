from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', login_required(views.ContactList.as_view()), name='contact-list'),
    # path('create/', login_required(views.DocsCreate.as_view()), name='docs-create'),
    path('update/<int:pk>/', login_required(views.ContactUpdate.as_view()), name='contact-update'),
    path('delete/<int:pk>/', login_required(views.ContactDelete.as_view()), name='contact-delete'),

    # Feedback
    path('feedback/', login_required(views.FeedbackList.as_view()), name='feedback-list'),
    path('feedback/update/<int:pk>/', login_required(views.FeedbackUpdate.as_view()), name='feedback-update'),
    path('feedback/delete/<int:pk>/', login_required(views.FeedbackDelete.as_view()), name='feedback-delete'),

    # Reception
    path('reception/create/', login_required(views.ReceptionCreate.as_view()), name='reception-create'),
    path('reception/', login_required(views.ReceptionList.as_view()), name='reception-list'),
    path('reception/update/<int:pk>/', login_required(views.ReceptionUpdate.as_view()), name='reception-update'),
    path('reception/delete/<int:pk>/', login_required(views.ReceptionDelete.as_view()), name='reception-delete'),

]
