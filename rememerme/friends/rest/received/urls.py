from django.conf.urls import patterns, include, url

from rememerme.friends.rest.received import views

urlpatterns = patterns('',
    url(r'^/?$', views.ReceivedListView.as_view()),
    url(r'^/(?P<user_id>[-\w]+)/?$', views.ReceivedSingleView.as_view())
)
