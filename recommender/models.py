from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from tastypie.models import create_api_key
from recommender.vendor.djangoratings.fields import RatingField

from recommender.vendor.djangoratings.models import Vote
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum, Count
import numpy as np
from recommender.algorithms.rating_inference import intervals

# Ensure that api keys are created on user creation
models.signals.post_save.connect(create_api_key, sender=User)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    bio = models.CharField(max_length=500, blank=True, null=True)
    url = models.URLField(max_length=500, blank=True, null=True)

    def __unicode__(self):
        return "Profile - %s" % (self.user)

class Feature(models.Model):
    name = models.TextField(unique=True)

    class Meta:
        verbose_name = 'Video Game Feature'

    def __unicode__(self):
        return self.name

class Platform(models.Model):
    name = models.CharField(max_length=512, unique=True)
    slug = models.SlugField(max_length=255)

    class Meta:
        verbose_name = 'Video Game Platform'

    def __unicode__(self):
        return self.name

class Specification(models.Model):
    name = models.TextField(unique=True)

    class Meta:
        verbose_name = 'Video Game Specification'

    def __unicode__(self):
        return self.name

class VideoGameRankingManager(models.Manager):
    def get_query_set(self):
        return super(VideoGameRankingManager, self).get_query_set().filter(~Q(name='') &
                                                                           ~Q(description='') &
                                                                           Q(ign_image__isnull=False))



    def smart_rating_order(self, limit=10):
        video_game_type = ContentType.objects.get(app_label="recommender", model="videogame")
        votes = Vote.objects.filter(content_type=video_game_type).values('object_id').annotate(S=Sum('score'), N=Count('object_id')).values_list('S', 'N', 'object_id')

        if votes:
            r = np.core.records.fromrecords(votes, names=['S', 'N', 'object_id'])

            # Approximate lower bounds
            posterior_mean, std_err  = intervals(r.S,r.N)
            lb = posterior_mean - std_err

            order = np.argsort( -lb )
            ordered_objects = []
            object_ids = r.object_id
            for i in order[:limit]:
                ordered_objects.append( object_ids[i] )

            objects = VideoGame.objects.in_bulk(ordered_objects)
            sorted_objects = [objects[id] for id in ordered_objects]

            return sorted_objects
        else:
            return VideoGame.ranked.order_by('-rating_votes')[:limit]

class VideoGame(models.Model):
    # Set VideoGame Managers
    objects = models.Manager()
    ranked = VideoGameRankingManager()

    # Fields
    name = models.CharField(max_length=500)
    description = models.TextField()
    ign_url = models.CharField(max_length=500, unique=True, help_text="The relative url for this game at http://www.ign.com")

    developer = models.CharField(max_length=255, blank=True, null=True)
    developer_url = models.URLField(blank=True, null=True)
    esrb_rating = models.DecimalField(decimal_places=3, max_digits=6, blank=True, null=True)
    esrb_rating_description = models.TextField(blank=True, null=True)
    features = models.ManyToManyField(Feature, blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True, null=True)
    genre_slug = models.SlugField(max_length=255)
    ign_community_rating = models.DecimalField(decimal_places=3, max_digits=6, blank=True, null=True)
    ign_community_rating_count = models.IntegerField(blank=True, null=True)
    ign_games_you_may_like = models.ManyToManyField('self', blank=True, null=True)
    ign_image = models.URLField(blank=True, null=True)
    ign_rating = models.DecimalField(decimal_places=3, max_digits=6, blank=True, null=True)
    ign_subheadline = models.CharField(max_length=255, blank=True, null=True)
    ign_wiki_edits = models.IntegerField(blank=True, null=True)
    platforms = models.ManyToManyField(Platform, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    publisher_url = models.URLField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    release_date_malformed = models.CharField(max_length=255, blank=True, null=True, help_text="This represents a release_date that might not be parseable into a date.")
    slug = models.SlugField(max_length=255)
    specifications = models.ManyToManyField(Specification, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    rating = RatingField(range=5,
                         can_change_vote=True,
                         allow_anonymous = True,
                         use_cookies = True)

    class Meta:
        verbose_name = "Video Game"
        verbose_name_plural = "Video Games"
        ordering = ('-name', '-ign_image', '-ign_rating')

    def __unicode__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User)
    video_game = models.ForeignKey(VideoGame)
    rating = RatingField(range=5, can_change_vote=True)
    comments = models.TextField(null=True, blank=True)

    def __unicode__():
        return '%s - %s' % (self.user, self.video_game)
