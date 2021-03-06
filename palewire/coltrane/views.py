# Helpers
import time
import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

# To add context from our context_processors
from django.template import RequestContext

# Models
from django.db.models import get_model
from tagging.models import Tag, TaggedItem
from coltrane.models import *
# Views
from django.views.generic.list_detail import object_list


def index(request):
    """
    The homepage.
    """
    group_list = [
        {'obj':Post, 'n':7},
        {'obj':Shout, 'n':5},
        {'obj':Commit, 'n':4},
        {'obj':Project, 'n':4},
        {'obj':Track, 'n':6},
        {'obj':Link, 'n':5}
    ]

    object_list = [{
            'name': group['obj'].__name__, 
            'objects': group['obj'].objects.all()[:group['n']],
            'root_url': reverse('coltrane_%s_root' % group['obj'].__name__.lower())
        } for group in group_list
    ]

    return render_to_response('coltrane/index.html', {'object_list':object_list}, context_instance=RequestContext(request))


def post_detail(request, year, month, day, slug):
    """
    A detail page that shows an entire post.
    """
    date_stamp = time.strptime(year+month+day, "%Y%m%d")
    pub_date = datetime.date(*date_stamp[:3])
    post = get_object_or_404(Post,  pub_date__year=pub_date.year,
                                    pub_date__month=pub_date.month,
                                    pub_date__day=pub_date.day,
                                    slug=slug)
    related_posts = TaggedItem.objects.get_related(post, get_model('coltrane', 'post'))[:5]
    return render_to_response('coltrane/post_detail.html',
                                { 'object': post,
                                  'related_posts': related_posts },
                                context_instance=RequestContext(request))
                                

def project_detail(request, slug):
    proj = Project.objects.get(slug=slug)
    return render_to_response("coltrane/project_detail.html", {'object':proj})


def category_detail(request, slug):
    """
    A list that reports all the posts in a particular category.
    """
    category = get_object_or_404(Category, slug=slug)
    return object_list(request, queryset = category.post_set.all(), 
                        extra_context = {'category': category },
                        template_name = 'coltrane/category_detail.html')


def tag_detail(request, tag):
    """
    A list that reports all of the content with a particular tag.
    """
    # Pull the tag
    tag = tag.replace("-", " ")
    tag = get_object_or_404(Tag, name=tag)
    
    # Pull all the items with that tag.
    taggeditem_list = tag.items.all()
    
    # Loop through the tagged items and return just the items
    object_list = [i.object for i in taggeditem_list if getattr(i.object, 'pub_date', False)]
    
    # Now resort them by the pub_date attribute we know each one should have
    object_list.sort(key=lambda x: x.pub_date, reverse=True)

    # Pass it out
    return render_to_response('coltrane/tag_detail.html', { 
            'tag': tag, 
            'object_list': object_list,
        })
        
