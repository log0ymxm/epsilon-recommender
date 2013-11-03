from django.db import models
from attributes.models import AttributeOption
from recommender.auth import CustomUser
from recommender.vendor.djangoratings.fields import RatingField

class VideoGame(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    ign_url = models.CharField(max_length=500, unique=True, help_text="The relative url for this game at http://www.ign.com")

    class Meta:
        verbose_name = "Video Game"
        verbose_name_plural = "Video Games"

    def __unicode__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(CustomUser)
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
