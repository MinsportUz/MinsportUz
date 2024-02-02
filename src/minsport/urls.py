"""minsport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
# from admin_panel.typo.views import TypoView


# from front.error.views import handler404 as page404
# handler404 = 'front.error.views.handler404'
# handler500 = 'front.error.views.handler500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),

    # path('error/', TypoView.as_view(), name='typo_reporting_form_url'),
]

urlpatterns += i18n_patterns(
    path('panel/', include('admin_panel.urls')),
    # path('', include('front.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
