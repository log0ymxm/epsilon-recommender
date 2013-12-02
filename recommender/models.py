from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from tastypie.models import create_api_key
from djangoratings.fields import RatingField
from djangoratings.models import Vote
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum, Count
import numpy as np
from recommender.algorithms.rating_inference import intervals
from recommender.managers import VideoGameRankingManager

# Ensure that api keys are created on user creation
models.signals.post_save.connect(create_api_key, sender=User)

class Platform(models.Model):
    name = models.CharField(max_length=512, unique=True)
    slug = models.SlugField(max_length=255)

    class Meta:
        verbose_name = 'Video Game Platform'

    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    url = models.URLField(max_length=500, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    about_you = models.TextField(blank=True, null=True)
    platforms_owned = models.ManyToManyField(Platform, blank=True, null=True)

    def __unicode__(self):
        return "Profile - %s" % (self.user)

class Genre(models.Model):
    name = models.TextField(unique=True)
    slug = models.SlugField(max_length=255)

    class Meta:
        verbose_name = 'Video Game Genre'

    def __unicode__(self):
        return self.name

class Feature(models.Model):
    name = models.TextField(unique=True)

    class Meta:
        verbose_name = 'Video Game Feature'

    def __unicode__(self):
        return self.name

class Specification(models.Model):
    name = models.TextField(unique=True)
    slug = models.SlugField(max_length=255)

    class Meta:
        verbose_name = 'Video Game Specification'

    def __unicode__(self):
        return self.name

class Company(models.Model):
    name = models.TextField(unique=True)
    url = models.URLField(blank=True, null=True)
    slug = models.SlugField(max_length=255)

    def __unicode__(self):
        return self.name

class ESRBRating(models.Model):
    rating = models.DecimalField(decimal_places=3, max_digits=6, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.value


class VideoGame(models.Model):
    # Set VideoGame Managers
    objects = models.Manager()
    ranked = VideoGameRankingManager()

    # Fields
    ign_url = models.CharField(max_length=500, unique=True, help_text="The relative url for this game at http://www.ign.com")
    ign_community_rating = models.DecimalField(decimal_places=3, max_digits=6, blank=True, null=True)
    ign_community_rating_count = models.IntegerField(blank=True, null=True)
    ign_image = models.URLField(blank=True, null=True)
    ign_rating = models.DecimalField(decimal_places=3, max_digits=6, blank=True, null=True)
    ign_subheadline = models.CharField(max_length=255, blank=True, null=True)
    ign_wiki_edits = models.IntegerField(blank=True, null=True)

    rating = RatingField(range=5, can_change_vote=True, allow_anonymous = True, use_cookies = True)

    name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=255)
    release_date = models.DateField(blank=True, null=True)
    release_date_malformed = models.CharField(max_length=255, blank=True, null=True, help_text="This represents a release_date that might not be parseable into a date.")
    description = models.TextField()
    summary = models.TextField(blank=True, null=True)

    features = models.ManyToManyField(Feature, blank=True, null=True)
    ign_games_you_may_like = models.ManyToManyField('self', blank=True, null=True)
    platforms = models.ManyToManyField(Platform, blank=True, null=True)
    specifications = models.ManyToManyField(Specification, blank=True, null=True)
    publisher = models.ManyToManyField(Company, blank=True, null=True, related_name='publisher')
    developer = models.ManyToManyField(Company, blank=True, null=True, related_name='developer')

    esrb_rating = models.ForeignKey(ESRBRating, blank=True, null=True)
    genre = models.ForeignKey(Genre, blank=True, null=True)
    # End Fields

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

    def __unicode__(self):
        return '%s - %s' % (self.user, self.video_game)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
