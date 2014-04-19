from django.conf.urls import patterns, url
from portal import views

# Base url is /home/
urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^home.html$', views.home),
    url(r'^about_me.html$', views.about_me),
    url(r'^development(/?)(?P<page_number>[0-9]*).html$', views.development),
    url(r'^life_record(/?)(?P<page_number>[0-9]*).html$', views.life_record),
    url(r'^article/(?P<id>[a-zA-Z0-9]+).html$', views.article),
    url(r'^tags.html$', views.tags),
    url(r'^search(/?)(?P<page_number>[0-9]*)$', views.search),
    url(r'^read_counter', views.read_counter),
    url(r'^test$', views.testbae),
)
