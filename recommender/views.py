from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from recommender.forms import SearchForm

from recommender.models import VideoGame

def home(request):
    title = "Home"
    popular_titles = VideoGame.objects.order_by('-rating_score')[:4]
    new_titles = VideoGame.objects.order_by('-release_date')[:4]

    return render_to_response('home.html',
                              locals(),
                              context_instance=RequestContext(request))

def recommendations(request):
    title = "Recommendations"
    video_games = VideoGame.objects.all().order_by('?')[:8]

    return render_to_response('recommendations.html',
                              locals(),
                              context_instance=RequestContext(request))

def search(request):
    title = "Search"


    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            video_games = VideoGame.objects.all()
            if form.cleaned_data['title']:
                video_games = video_games.filter(name__icontains=form.cleaned_data['title'])
            if form.cleaned_data['release_date']:
                video_games = video_games.filter(release_date__icontains=form.cleaned_data['release_date'])
            if form.cleaned_data['platform']:
                video_games = video_games.filter(platforms=form.cleaned_data['platform'])
            if form.cleaned_data['genre']:
                video_games = video_games.filter(genre__icontains=form.cleaned_data['genre'])

            video_games = video_games[:20]
    else:
        form = SearchForm()
        video_games = None


    return render_to_response('search.html',
                              locals(),
                              context_instance=RequestContext(request))

def genre(request, slug):
    title = "Genre"
    video_games = VideoGame.objects.filter(genre_slug = slug)

    return render_to_response('genre.html',
                              locals(),
                              context_instance=RequestContext(request))

def game_detail_page(request):
    title = "Game Detail Page"

    v = VideoGame.objects.all()[0]

    return render_to_response('game_detail_page.html',
                              locals(),
                              context_instance=RequestContext(request))
