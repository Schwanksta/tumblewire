import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField
from tagging.models import Tag

from django.db import models

from coltrane.managers import LivePostManager, LiveCategoryManager, SyncManager

from django.db.models import signals
from coltrane.signals import create_ticker_item, delete_ticker_item, category_count


class Ticker(models.Model):
	"""
	A tumblelog of the latest content items, pushed automagically by the functions in signals.py.
	
	This is what populates the front page of the blog.
	"""
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	pub_date = models.DateTimeField()
	content_object = generic.GenericForeignKey('content_type', 'object_id')

	class Meta:
		verbose_name_plural = _('Ticker')

	def __unicode__(self):
		return u'%s: %s' % (self.content_type.model_class().__name__, self.content_object)

	def get_rendered_html(self):
		template_name = 'coltrane/ticker_item_%s.html' % (self.content_type.name)
		return render_to_string(template_name, { 'object': self.content_object })


class Slogan(models.Model):
	"""
	The slogans that randomly appear at the top of the blog when the logo is hovered over.
	"""
	title = models.CharField(max_length=250, help_text=_('Maximum 250 characters.'))

	class Meta:
		ordering = ['title']
		
	def __unicode__(self):
		return self.title
		


class Category(models.Model):
	"""
	Topic labels for grouping blog entries.
	"""
	title = models.CharField(max_length=250, help_text=_('Maximum 250 characters.'))
	slug = models.SlugField(unique=True, help_text=_('Suggested value automatically generated from title. Must be unique.'))
	description = models.TextField(null=True, blank=True)
	post_count = models.IntegerField(default=0, editable=False)
	objects = models.Manager()
	live = LiveCategoryManager()
	
	class Meta:
		ordering = ['title']
		verbose_name_plural = _('Categories')
		
	def __unicode__(self):
		return self.title
		
	def get_absolute_url(self):
		return u"/categories/%s/" % self.slug
		
	def get_absolute_icon(self):
		return u'/media/icons/categories.gif'

	def get_live_post_count(self):
		from coltrane.models import Post
		return Post.live.filter(categories=self).count()


class Post(models.Model):
	"""
	Blog posts. For longer stuff I write. 
	
	Supports pygments by placing code in <pre lang="xxx"> tags.
	"""
	LIVE_STATUS = 1
	DRAFT_STATUS = 2
	HIDDEN_STATUS = 3
	STATUS_CHOICES = (
		(LIVE_STATUS, 'Live'),
		(DRAFT_STATUS, 'Draft'),
		(HIDDEN_STATUS, 'Hidden'),
	)
	
	wordpress_id = models.IntegerField(unique=True, null=True, blank=True, help_text=_('The junky old wp_posts id from before the migration'), editable=False)
	title = models.CharField(max_length=250, help_text=_('Maximum 250 characters.'))
	slug = models.SlugField(max_length=300, unique_for_date='pub_date', help_text=_('Suggested value automatically generated from title.'))
	body_markup = models.TextField(help_text=_('The HTML of the post that is edited by the author.'))
	body_html = models.TextField(null=True, blank=True, editable=False, help_text=_('The HTML of the post after it has been run through Pygments.'))
	pub_date = models.DateTimeField(verbose_name=_('publication date'), default=datetime.datetime.now)
	author = models.ForeignKey(User)
	enable_comments = models.BooleanField(default=True)
	status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS, help_text=_("Only entries with 'Live' status will be publicly displayed."))
	categories = models.ManyToManyField(Category)
	tags = TagField(help_text=_('Separate tags with spaces.'), blank=True)
	objects = models.Manager()
	live = LivePostManager()

	class Meta:
		ordering = ['-pub_date']
	
	def __unicode__(self):
		return self.title

	def save(self, force_insert=False, force_update=False):
		from coltrane.utils.pygmenter import pygmenter
		self.body_html = pygmenter(self.body_markup)
		super(Post, self).save()
				
	def get_absolute_url(self):
		return ('coltrane_post_detail', (), { 'year': self.pub_date.strftime("%Y"),
												'month': self.pub_date.strftime("%m"),
												'day': self.pub_date.strftime("%d"),
												'slug': self.slug })
												
	get_absolute_url = models.permalink(get_absolute_url)
	
	def get_absolute_icon(self):
		return u'/media/icons/posts.gif'
		
	def get_tags(self):
		return Tag.objects.get_for_object(self)


class ThirdPartyBaseModel(models.Model):
	"""
	A base model for the data we'll be pulling from third-party sites.
	"""
	url = models.URLField(unique=True, max_length=1000)
	pub_date = models.DateTimeField(default=datetime.datetime.now)
	tags = TagField(help_text=_('Separate tags with spaces.'), max_length=1000)
	sync = SyncManager()
	objects = models.Manager()
	
	class Meta:
		ordering = ('-pub_date',)
		abstract = True
		
	def get_tags(self):
		return Tag.objects.get_for_object(self)
	

class Shout(ThirdPartyBaseModel):
	"""
	Shorter things I blast out.
	"""
	message = models.TextField(max_length=140)

	def __unicode__(self):
		return self.message

	def get_absolute_icon(self):
		return u'/media/icons/shouts.gif'


class Photo(ThirdPartyBaseModel):
	"""
	Links to photos I want to recommend, including my own.
	"""
	title = models.CharField(max_length=250, blank=True, null=True)
	description = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return self.title
	
	def get_absolute_icon(self):
		return u'/media/icons/photos.gif'


class Track(ThirdPartyBaseModel):
	"""
	Links to tracks I've listened to and logged at Last.fm.
	"""
	artist_name = models.CharField(max_length=250)
	track_name = models.CharField(max_length=250)
	track_mbid = models.CharField(verbose_name = _("MusicBrainz Track ID"), max_length=36, blank=True)
	artist_mbid = models.CharField(verbose_name = _("MusicBrainz Artist ID"), max_length=36, blank=True)

	def __unicode__(self):
		return u"%s - %s" % (self.artist_name, self.track_name)
		
	def get_absolute_icon(self):
		return u'/media/icons/tracks.gif'


class Link(models.Model):
	"""
	Links to bookmarks I'd like to recommend.
	"""
	title = models.CharField(max_length=250)
	description = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return self.title
			
	def get_absolute_icon(self):
		return u'/media/icons/links.gif'
		

# Signals
for modelname in [Link, Photo, Post, Shout, Track, Comment]:
	signals.post_save.connect(create_ticker_item, sender=modelname)
	
for modelname in [Link, Photo, Post, Shout, Track, Comment]:
	signals.post_delete.connect(delete_ticker_item, sender=modelname)

signals.post_save.connect(category_count, sender=Post)
signals.post_delete.connect(category_count, sender=Post)

# Comment moderation
from comment_utils.moderation import CommentModerator, moderator, AlwaysModerate
class ColtraneModerator(AlwaysModerate):
	#akismet = True
	email_notification = True
	enable_field = 'enable_comments'

moderator.register(Post, ColtraneModerator)
