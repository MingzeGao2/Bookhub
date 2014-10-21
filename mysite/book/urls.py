from django.conf.urls import patterns, url

from book import views

urlpatterns = patterns('',
                       url(r'^need/(?P<ISBN>.*)/$', views.need, name = 'need'),
                       url(r'^have/(?P<ISBN>.*)/$',views.have, name = 'have'),
                       url(r'^delete/(?P<ISBN>.*)/$', views.delete, name = 'delete'),
                      
)