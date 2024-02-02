from django.contrib.auth.decorators import login_required
from django.urls import path, include

from admin_panel.app import about
from admin_panel.app.auth.views import Login, Logout, Profile
from admin_panel.app.index.views import Index

# Registering namespace for URL

urlpatterns = [
    # path('api/', include('api.urls')),
    # path('get_image_url/', TinymceImageCreate.as_view(), name='get-image-url'),
    # path('search/', Search.as_view(), name='search'),

    path('', login_required(Index.as_view()), name='index-admin'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', login_required(Logout.as_view()), name='logout'),
    path('profile/', login_required(Profile.as_view()), name='profile'),
    path('about/', include('admin_panel.app.about.urls', namespace='about')),
    path('news/', include('admin_panel.app.news.urls', namespace='news')),
    path('gallery/', include('admin_panel.app.gallery.urls', namespace='gallery')),
    path('vacancy/', include('admin_panel.app.vacancy.urls', namespace='vacancy')),
    path('service/', include('admin_panel.app.service.urls', namespace='service')),
    path('docs/', include('admin_panel.app.docs.urls', namespace='docs')),
    path('sport/', include('admin_panel.app.sport.urls', namespace='sport')),
    path('event/', include('admin_panel.app.event.urls', namespace='event')),
    path('tender/', include('admin_panel.app.tender.urls', namespace='tender')),
    path('link/', include('admin_panel.app.link.urls', namespace='link')),
    path('region/', include('admin_panel.app.region.urls', namespace='region')),
    path('district/', include('admin_panel.app.district.urls', namespace='district')),
    path('regionaldepartment/', include('admin_panel.app.regionaldepartment.urls', namespace='regionaldepartment')),
    path('typo/', include('admin_panel.app.typo.urls', namespace='typo')),
    path('static/', include('admin_panel.app.static_page.urls', namespace='static')),
    path('menu/', include('admin_panel.app.menu.urls', namespace='menu')),
    path('quizz/', include('admin_panel.app.quizz.urls', namespace='quizz')),
    path('settings/', include('admin_panel.app.settings.urls', namespace='settings')),
    path('contact/', include('admin_panel.app.contact.urls', namespace='contact')),
    path('user/', include('admin_panel.app.user.urls', namespace='user')),

]
