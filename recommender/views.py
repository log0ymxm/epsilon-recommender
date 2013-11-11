from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q

from recommender.models import VideoGame

def home(request):
    title = "Home"
    video_games = VideoGame.objects.filter(~Q(name='') &
                                            ~Q(description='') &
                                            Q(ign_image__isnull=False)
                                            ).order_by('?')[:8]

    return render_to_response('home.html',
                              locals(),
                              context_instance=RequestContext(request))

def recommendations(request):
    title = "Recommendations"
    video_games = VideoGame.objects.filter(~Q(name='') &
                                            ~Q(description='') &
                                            Q(ign_image__isnull=False)
                                            ).order_by('?')[:8]

    return render_to_response('recommendations.html',
                              locals(),
                              context_instance=RequestContext(request))

def search(request):
    title = "Search"
    video_games = VideoGame.objects.filter(~Q(name='') &
                                            ~Q(description='') &
                                            Q(ign_image__isnull=False)
                                            ).order_by('?')[:8]

    return render_to_response('search.html',
                              locals(),
                              context_instance=RequestContext(request))
