from django.db import models
from attributes.models import AttributeOption
from django.contrib.auth.models import User
from tastypie.models import create_api_key
from recommender.vendor.djangoratings.fields import RatingField

# Ensure that api keys are created on user creation
models.signals.post_save.connect(create_api_key, sender=User)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    bio = models.CharField(max_length=500, blank=True, null=True)
    url = models.URLField(max_length=500, blank=True, null=True)

    def __unicode__(self):
        return "Profile - %s" % (self.user)

class VideoGame(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    ign_url = models.CharField(max_length=500, unique=True, help_text="The relative url for this game at http://www.ign.com")

    class Meta:
        verbose_name = "Video Game"
        verbose_name_plural = "Video Games"
        ordering = ('name',)

    def __unicode__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User)
    video_game = models.ForeignKey(VideoGame)
    rating = RatingField(range=5, can_change_vote=True)
    comments = models.TextField(null=True, blank=True)

    def __unicode__():
        return '%s - %s' % (self.user, self.video_game)

class VideoGameAttribute(models.Model):
    video_game = models.ForeignKey(VideoGame)
    option = models.ForeignKey(AttributeOption)
    value = models.TextField()

    def _name(self):
        return self.option.name
    name = property(_name)

    def _description(self):
        return self.option.description
    description = property(_description)

    class Meta:
        verbose_name = "Video Game Attribute"
        verbose_name_plural = "Video Game Attributes"
        ordering = ('option__sort_order',)

    def __unicode__(self):
        return self.option.name
