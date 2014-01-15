from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'NomNomUsers.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^rest/v1/', include('rememerme.friends.rest.urls')),
)
