from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from recommender.forms import SearchForm

from recommender.models import VideoGame

def home(request):
    title = "Home"
    video_games = VideoGame.objects.filter(~Q(name='') &
                                            ~Q(description='') &
                                            Q(ign_image__isnull=False)
                                            ).order_by('?')[:4]

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

    
    if request.method == 'POST': # If the form has been submitted...
        form = SearchForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            video_games = VideoGame.objects.filter(name  = form.cleaned_data['title'])
    else:
        form = SearchForm() # An unbound form
        video_games = None


    return render_to_response('search.html',
                              locals(),
                              context_instance=RequestContext(request))

def genre(request, slug):
    title = "Genre"
    video_games = VideoGame.objects.filter(genre_slug = slug)

    return render_to_response('genre.html', 
                              locals(), 
    
def game_detail_page(request):
    title = "Game Detail Page"
    
    v = VideoGame.objects.filter(~Q(name='') &
                                           ~Q(description=''))[0]
   
    return render_to_response('game_detail_page.html',
                              locals(),
                              context_instance=RequestContext(request))
    
