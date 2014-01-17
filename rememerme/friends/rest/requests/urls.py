from django.conf.urls import patterns, include, url

from rememerme.friends.rest.requests import views

urlpatterns = patterns('',
    url(r'^$', views.RequestsListView.as_view()),
    url(r'^/$', views.RequestsListView.as_view())
)
