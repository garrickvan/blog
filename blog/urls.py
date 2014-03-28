from django.conf.urls import patterns, include, url
from django.contrib import admin
from blog import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^manage_site/', include(admin.site.urls)),
    url(r'^', include('portal.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        url(r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )
