from coltrane.blog_settings import site_name, site_domain, meta_info, feeds, my_full_name

def site_info(request):
    return {'site_name': site_name, 'site_domain': site_domain, 'my_full_name': my_full_name}

def meta(request):
    return {'meta_info': meta_info}

def feed_autodiscover(request):
    # Weirdest thing ever. 'feeds' has to be used once (even just by putting it on a blank line)
    # before it'll populate. I don't know if I get it...
    feeds
    return {'feeds': feeds} 
