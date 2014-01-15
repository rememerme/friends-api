from django.conf.urls import patterns, include, url

from rememerme.users.rest import views

urlpatterns = patterns('',
    url(r'^$', views.UsersListView.as_view()),
    url(r'^(?P<user_id>[-\w]+)/$', views.UsersSingleView.as_view()),
    url(r'^(?P<user_id>[-\w]+)$', views.UsersSingleView.as_view())
)
