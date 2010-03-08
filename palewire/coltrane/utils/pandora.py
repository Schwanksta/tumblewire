import datetime
import urllib
import logging
import os
import sys

# Set the directories and django config so it can be run from cron.
current_dir = os.path.abspath(__file__)
projects_dir = os.sep.join(current_dir.split(os.sep)[:-3])
os.environ['PYTHONPATH'] = projects_dir
sys.path.append(projects_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.conf import settings
from django.db import transaction
from django.utils.encoding import smart_unicode
from httplib2 import HttpLib2Error
from coltrane import utils
from coltrane.models import Track
from django.template.defaultfilters import slugify
from django.utils.functional import memoize
from django.utils.http import urlquote

#
# API URLs
#
 
BOOKMARKED_TRACKS_URL = "http://feeds.pandora.com/feeds/people/%s/favorites.xml"
 
#
# Public API
#
 
log = logging.getLogger("coltrane.utils.lastfm")
 
def enabled():
    return hasattr(settings, 'PANDORA_USER')
 
def update():
    last_update_date = Track.sync.get_last_update()
    log.debug("Last update date: %s", last_update_date)
    
    xml = utils.getxml(BOOKMARKED_TRACKS_URL % settings.PANDORA_USER)
    for track in xml.getiterator("item"):
        artist = track.find('{http://musicbrainz.org/mm/mm-2.1#}Artist').find('{http://purl.org/dc/elements/1.1/}title')
        artist_name = smart_unicode(artist.text)
        track_name = smart_unicode(track.find('{http://musicbrainz.org/mm/mm-2.1#}Track').find('{http://purl.org/dc/elements/1.1/}title').text)
        album_name = smart_unicode(track.find('{http://musicbrainz.org/mm/mm-2.1#}Album').find('{http://purl.org/dc/elements/1.1/}title').text)
        url = smart_unicode(track.find('link').text)
        pdate = track.find('pubDate').text.split('-')[0].strip()
        timestamp = datetime.datetime.strptime(pdate, "%a, %d %b %Y %H:%M:%S")
        if timestamp > last_update_date:
            log.debug("Handling track: %r - %r", artist_name, track_name)
            _handle_track(artist_name, track_name, album_name, url, timestamp)
 
#
# Private API
#
 
@transaction.commit_on_success
def _handle_track(artist_name, track_name, album_name, url, timestamp):
    t, created = Track.objects.get_or_create(
        artist_name = artist_name,
        track_name = track_name,
        album_name = album_name,
        pub_date = timestamp,
        url = url,
    )
    if created == True:
         print u'Logged %s - %s' % (artist_name, track_name)
    else:
         print "Failed to log the track %s - %s" %  (artist_name, track_name)

if __name__ == '__main__':
    update()
