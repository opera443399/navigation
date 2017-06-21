"""localmonitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import ugettext_lazy as _

from portal import views as portal_views

admin.site.site_header = _('Portal Management')
admin.site.index_title = _('Site Admin')
admin.site.site_title = _('Portal')

# ================================ URL ================================
urlpatterns = [
    #################################### index
    #
    url(r'^$', portal_views.show_index, name='index'),
    #################################### apps
    #
    url(r'^portal/', include('portal.urls')),
    #################################### admin
    #
    url(r'^admin/', include(admin.site.urls)),
    #################################### i18n
    #
    url(r'^i18n/', include('django.conf.urls.i18n')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
