import os
this_dir = os.path.dirname(__file__)

from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from coltrane.sitemaps import sitemaps

urlpatterns = patterns('',

	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/(.*)', admin.site.root),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
	
	(r'^books/', include('coltrane.urls.books')),
	(r'^categories/', include('coltrane.urls.categories')),
	(r'^links/', include('coltrane.urls.links')),
	(r'^tags/', include('coltrane.urls.tags')),
	(r'^posts/', include('coltrane.urls.posts')),
	(r'^shouts/', include('coltrane.urls.shouts')),
	(r'^photos/', include('coltrane.urls.photos')),
	(r'^tracks/', include('coltrane.urls.tracks')),

	(r'^comments/page/', include('coltrane.urls.comments')),
	(r'^comments/', include('django.contrib.comments.urls')),

	(r'^$', include('coltrane.urls.index')),
	(r'^ticker/', include('coltrane.urls.ticker')),

#	(r'^search/', include('solango.urls')),
	(r'^feeds/', include('coltrane.urls.feeds')),
	(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
	#(r'^robots.txt$', include('robots.urls')),

)
