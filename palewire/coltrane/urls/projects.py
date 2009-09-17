from django.conf.urls.defaults import *

from coltrane.models import Project

index_dict = {
	'queryset': Project.objects.all().order_by("status__val"),
	'paginate_by': 25,
}


urlpatterns = patterns('django.views.generic',

	# The root url
	url(r'^$', 'simple.redirect_to', { 'url': '/projects/page/1/' }, name='coltrane_project_root'),

	# List
	url(r'^page/(?P<page>[0-9]+)/$', 'list_detail.object_list', index_dict, name='coltrane_project_list'),

)

urlpatterns += patterns('coltrane.views',
	url(r'^detail/(?P<slug>[-\w]+)/$', 
		'project_detail', name='coltrane_project_detail'),
)



