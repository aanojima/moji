from django.conf.urls import patterns, include, url
import views
from django.contrib import admin
admin.autodiscover()

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'Moji.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/^$', views.login),
    url(r'^logout/^$', views.logout),
    url(r'^signup/^$', views.signup),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)