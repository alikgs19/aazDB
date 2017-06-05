from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.donothing, name='index'),
    url(r'^getteams/$', views.getteams, name='getteams'),
    url(r'^getclubinfo/$', views.getclubinfo, name='getclubinfo'),
    url(r'^playmatch/$', views.playmatch, name='playmatch'),
]