# Feeds
from django.contrib.syndication.feeds import Feed

# Models
from coltrane.models import *
from django.contrib.comments.models import Comment

# Site name
from coltrane.blog_settings import site_name, site_domain


class FullFeed(Feed):
	title = "%s.full_feed" % site_name
	link = "http:/%s/feeds/the-full-feed/" % site_domain
	description = "the latest from %s" % site_name

	def items(self):
		return Ticker.objects.all().order_by('-pub_date')[:10]

	def item_pubdate(self, item):
		return item.pub_date
		
	def item_link(self, item):
		try:
			return item.content_object.url
		except AttributeError:
			return item.content_object.get_absolute_url()


class LessNoise(Feed):
	title = "%s.less_noise" % site_name
	link = "http://%s/feeds/less-noise/" % site_domain
	description = "the latest from %s, except for all those tracks" % site_name

	def items(self):
		return Ticker.objects.exclude(content_type__name__iexact='Track').order_by('-pub_date')[:10]

	def item_pubdate(self, item):
		return item.pub_date

	def item_link(self, item):
		try:
			return item.content_object.url
		except AttributeError:
			return item.content_object.get_absolute_url()


class RecentPosts(Feed):
	title = "%s.posts" % site_name
	link = "http://%s/feeds/posts/" % site_domain
	description = "the latest posts at %s" % site_name

	def items(self):
		return Post.live.all().order_by('-pub_date')[:10]

	def item_pubdate(self, item):
		return item.pub_date


class RecentBooks(Feed):
	title = "%s.books" % site_name
	link = "http://%s/feeds/books/" % site_domain
	description = "the latest books at %s" % site_name

	def items(self):
		return Book.objects.all().order_by('-pub_date')[:10]

	def item_link(self, item):
		return item.url

	def item_pubdate(self, item):
		return item.pub_date


class RecentCommits(Feed):
	title = "%s.commits" % site_name
	link = "http://%s/feeds/commits/" % site_domain
	description = "the latest code commits at %s" % site_name

	def items(self):
		return Commit.objects.all().order_by('-pub_date')[:10]

	def item_link(self, item):
		return item.url

	def item_pubdate(self, item):
		return item.pub_date


class RecentShouts(Feed):
	title = "%s.shouts" % site_name
	link = "http://%s/feeds/shouts/" % site_domain
	description = "the latest shouts at %s" % site_name

	def items(self):
		return Shout.objects.all().order_by('-pub_date')[:10]

	def item_link(self, item):
		return item.url

	def item_pubdate(self, item):
		return item.pub_date


class RecentLinks(Feed):
	title = "%s.links" % site_name
	link = "http://%s/feeds/links/" % site_domain
	description = "the latest links at %s" % site_name

	def items(self):
		return Link.objects.all().order_by('-pub_date')[:10]

	def item_link(self, item):
		return item.url

	def item_pubdate(self, item):
		return item.pub_date


class RecentPhotos(Feed):
	title = "%s.photos" % site_name
	link = "http://%s/feeds/photos/" % site_domain
	description = "the latest photos at %s" % site_name

	def items(self):
		return Photo.objects.all().order_by('-pub_date')[:10]

	def item_link(self, item):
		return item.url

	def item_pubdate(self, item):
		return item.pub_date


class RecentTracks(Feed):
	title = "%s.tracks" % site_name
	link = "http://%s/feeds/tracks/" % site_domain
	description = "the latest tracks at %s" % site_name

	def items(self):
		return Track.objects.all().order_by('-pub_date')[:10]

	def item_link(self, item):
		return item.url

	def item_pubdate(self, item):
		return item.pub_date


class RecentComments(Feed):
	title = "%s.comments" % site_name
	link = "http://%s/feeds/comments" % site_domain
	description = "the latest comments at %s" % site_name

	def items(self):
		return Comment.objects.filter(is_public=True).order_by('-submit_date')[:10]
		
	def item_pubdate(self, item):
		return item.submit_date
