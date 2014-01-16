from django.conf.urls import patterns, include, url

from rememerme.friends.rest.sent import views

urlpatterns = patterns('',
    url(r'^$', views.FriendsListView.as_view()),
    url(r'^/$', views.FriendsListView.as_view()),
    url(r'^/(?P<user_id>[-\w]+)/$', views.FriendsSingleView.as_view()),
    url(r'^/(?P<user_id>[-\w]+)$', views.FriendsSingleView.as_view())
)
