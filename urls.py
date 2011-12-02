from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import content.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eurofunnel.views.home', name='home'),
    # url(r'^eurofunnel/', include('eurofunnel.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url( r'^click/(?P<article_id>[^/\^?]+)$', 'content.views.click', name='click' ),
    url( r'^tag/(?P<tag>[^/\^?]+)$', 'content.views.filter_tag', name='filter_tag' ),
    url( r'^source/(?P<source>.+)$', 'content.views.filter_source', name='filter_source' ),
    url( r'^search_autocomplete/$', 'content.views.search_autocomplete', name='search_autocomplete' ),
    url( r'^search/$', 'content.views.search', name='search' ),
    url( r'^$', 'content.views.home', name="home" ),
)
