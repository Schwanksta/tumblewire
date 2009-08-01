from django.conf.urls.defaults import *

from coltrane.models import Ticker

urlpatterns = patterns('',
	
	# The root url
	url(r'^$', 'coltrane.views.index', name='coltrane_index'),

)
