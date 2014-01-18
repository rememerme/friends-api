from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^rest/v1/friends/requests/sent', include('rememerme.friends.rest.sent.urls')),
    url(r'^rest/v1/friends/requests/received', include('rememerme.friends.rest.received.urls')),
    url(r'^rest/v1/friends/requests', include('rememerme.friends.rest.requests.urls')),
    url(r'^rest/v1/friends', include('rememerme.friends.rest.friends.urls'))
)
