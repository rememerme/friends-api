from django.conf.urls import patterns, url

from rememerme.friends.rest.sent import views

urlpatterns = patterns('',
    url(r'^/?$', views.SentListView.as_view()),
    url(r'^/(?P<user_id>[-\w]+)/?$', views.SentSingleView.as_view())
)
