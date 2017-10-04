from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.app_list, name='app_list'),
    url(r'^(?P<app_id>[0-9]+)/$', views.app, name='app')
]