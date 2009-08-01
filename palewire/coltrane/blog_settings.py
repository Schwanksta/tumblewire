# Site name
from settings import SITE_ID
from django.contrib.sites.models import Site

my_full_name = "Ken Schwencke"

this_site = Site.objects.get(pk=SITE_ID)
site_domain = this_site.domain
site_name = this_site.name

# Each of these corresponds to its HTML <meta> equivalent.
meta_info = {
    'author': 'schwanksta.com',
    'description': 'Ken Schwencke\'s slice of the Internet.',
    'keywords': 'schwanksta, ken schwencke, online journalism, journalism, django',
    'robots': 'index,nofollow' 
}

# Collects all feeds from coltrane.feeds into a list
from django.contrib.syndication.feeds import Feed
from inspect import isclass
import feeds as blog_feeds

feeds = [f for f in blog_feeds.__dict__.itervalues() if isclass(f) and issubclass(f, Feed) and hasattr(f, 'title')]

