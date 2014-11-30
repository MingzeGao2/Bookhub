from django.conf.urls import patterns, url

from book import views

urlpatterns = patterns('',
                       url(r'^need/$', views.need, name = 'need'),
                       url(r'^have/$',views.have, name = 'have'),
                       url(r'^delete/$', views.delete, name = 'delete'),
                       url(r'^insert/$',views.insert, name = 'insert'),
                       url(r'^insertbook/$',views.insertbook, name= 'insertbook'),
                       url(r'^delete/deletebook/$',views.deletebook, name='deletebook'),
                       url(r'^need/needbook/$', views.needbook, name='needbook'),
                       url(r'^have/havebook/$', views.havebook, name='havebook'),
                       url(r'^register/$',views.register,name='register'),
                       url(r'^signup/$',views.signup, name='signup'),
                       url(r'^login/$',views.login, name='login'),
                       url(r'^your_books/$', views.your_books, name='you_books'),
                       url(r'^your_wanted_list/$', views.your_wanted_list, name='your_wanted_list'),
                       url(r'^add_books/$',views.add_books, name="add_books"),
                       url(r'^your_account/$',views.your_account,name="your_account"),
                       url(r'enlargeDatabase/$',views.enlargeDatabase,name="enlargeDatabase"),
                       url(r'recommended_to_you/$',views.recommended_to_you,name="recommended_to_you"),
                       url(r'^$', views.index, name='index'),
)
