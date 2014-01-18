from django.conf.urls import patterns, url

from rememerme.friends.rest.friends import views

urlpatterns = patterns('',
    url(r'^/?$', views.FriendsListView.as_view()),
    url(r'^/(?P<user_id>[-\w]+)/?$', views.FriendsSingleView.as_view())
)
