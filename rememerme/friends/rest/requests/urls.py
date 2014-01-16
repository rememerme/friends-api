from django.conf.urls import patterns, include, url

from rememerme.friends.rest.requests import views

urlpatterns = patterns('',
    url(r'^$', views.FriendsListView.as_view()),
    url(r'^/$', views.FriendsListView.as_view())
)
