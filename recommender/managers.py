from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
import numpy as np
from recommender.models import Vote
from recommender.algorithms.rating_inference import intervals
from django.db.models import Sum, Count

class VideoGameRankingManager(models.Manager):
    def get_query_set(self):
        return super(VideoGameRankingManager, self).get_query_set().filter(~Q(name='') &
                                                                           ~Q(description='') &
                                                                           ~Q(slug='') &
                                                                           ~Q(ign_image='http://oystatic.ignimgs.com/src/core/img/widgets/global/page/ign-logo-100x100.jpg') &
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

            objects = self.get_query_set().in_bulk(ordered_objects)
            sorted_objects = [objects[id] for id in ordered_objects if id in objects]

            return sorted_objects
        else:
            return self.get_query_set().order_by('-rating_votes')[:limit]

