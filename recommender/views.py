from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q

from recommender.models import VideoGame

def home(request):
    title = "Home"

    # SELECT * FROM videio_game WHERE name is not null LIMIT 5
    video_games = VideoGame.objects.filter(~Q(name='') &
                                           ~Q(description=''))[:5]
    print '---', video_games

    return render_to_response('home.html',
                              locals(),
                              context_instance=RequestContext(request))

def recommendations(request):
    title = "Recommendations"
   
    return render_to_response('recommendations.html',
                              locals(),
                              context_instance=RequestContext(request))
