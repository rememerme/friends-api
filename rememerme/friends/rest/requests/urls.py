from django.conf.urls import patterns, url

from rememerme.friends.rest.requests import views

urlpatterns = patterns('',
    url(r'^/?$', views.RequestsListView.as_view())
)
