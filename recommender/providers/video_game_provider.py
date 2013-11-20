from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from recommends.providers import recommendation_registry, RecommendationProvider

from recommender.models import VideoGame
from djangoratings.models import Vote
from recommender.algorithms.probabilistic_collaborative_filtering import ProbabilisticMatrixFactorizationAlgorithm

class VideoGameRecommendationProvider(RecommendationProvider):
    algorithm = ProbabilisticMatrixFactorizationAlgorithm()

    def get_users(self):
        return User.objects.filter(is_active=True, votes__isnull=False).distinct()

    def get_items(self):
        return VideoGame.objects.all()

    # def items_ignored(self):
    # Returns user ignored items. User can delete items from the list of recommended.

    def get_ratings(self, obj):
        return Vote.objects.filter(object_id=obj.id)

    def get_rating_user(self, rating):
        return rating.user

    def get_rating_score(self, rating):
        return rating.score

    def get_rating_item(self, rating):
        return VideoGame.objects.get(pk=rating.object_id)

    def get_rating_site(self, rating):
        return Site.objects.get_current()

    # def is_rating_active(self, rating)

    # def pre_store_similarities(self, itemMatch)
    # stats or visualize

recommendation_registry.register(Vote, [VideoGame], VideoGameRecommendationProvider)
