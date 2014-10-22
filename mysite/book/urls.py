from django.conf.urls import patterns, url

from book import views

urlpatterns = patterns('',
                       url(r'^need/$', views.need, name = 'need'),
                       url(r'^have/$',views.have, name = 'have'),
                       url(r'^delete/$', views.delete, name = 'delete'),
                       url(r'^insert/$',views.insert, name = 'insert'),
                       url(r'^insert/insertbook/$',views.insertbook, name= 'insertbook'),
                       url(r'^delete/deletebook/$',views.deletebook, name='deletebook'),
                       url(r'^need/needbook/$', views.needbook, name='needbook'),
                       url(r'^have/havebook/$', views.havebook, name='havebook'),
                       url(r'^$', views.index, name='index'),
)
