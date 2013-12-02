from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from recommender.forms import SearchForm, UserProfileForm, ReviewForm
from recommender.models import Review


from recommender.models import VideoGame, Genre, UserProfile

def home(request):
    title = "Home"
    popular_titles = VideoGame.ranked.smart_rating_order(limit=4)
    new_titles = VideoGame.ranked.order_by('-release_date')[:4]
    random_titles = VideoGame.ranked.order_by('?')[:4]

    return render_to_response('home.html',
                              locals(),
                              context_instance=RequestContext(request))

def recommendations(request):
    title = "Recommendations"
    video_games = VideoGame.ranked.all().order_by('?')[:8]

    return render_to_response('recommendations.html',
                              locals(),
                              context_instance=RequestContext(request))

def search(request):
    title = "Search"


    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            video_games = VideoGame.ranked.all()
            if form.cleaned_data['title']:
                video_games = video_games.filter(name__icontains=form.cleaned_data['title'])
            if form.cleaned_data['release_date']:
                video_games = video_games.filter(release_date__icontains=form.cleaned_data['release_date'])
            if form.cleaned_data['platform']:
                video_games = video_games.filter(platforms=form.cleaned_data['platform'])
            if form.cleaned_data['genre']:
                video_games = video_games.filter(genre=form.cleaned_data['genre'])

            video_games = video_games[:20]
    else:
        form = SearchForm()
        video_games = None


    return render_to_response('search.html',
                              locals(),
                              context_instance=RequestContext(request))

def genre_detail(request, slug=None):
    title = "Genre"
    if slug:
        video_games = VideoGame.ranked.filter(genre__slug = slug)
        genre = Genre.objects.get(slug = slug)
    else:
        video_games = VideoGame.ranked.all()[:10]

    return render_to_response('genre_detail.html',
                              locals(),
                              context_instance=RequestContext(request))

def genre(request):
    title = "Genre"
    video_games = VideoGame.ranked.smart_rating_order(limit=4)

    return render_to_response('genre.html',
                              locals(),
                              context_instance=RequestContext(request))

def game_detail_page(request, slug):
    title = "Game Detail Page"

    v = VideoGame.ranked.filter(slug=slug)[0]

    if request.method == 'POST':
      form = ReviewForm(request.POST)
      if form.is_valid():
        review, created = Review.objects.get_or_create(user = request.user, video_game = v)
        review.comments = form.cleaned_data['review']
        review.save()
        pass
    else:
       form = ReviewForm()

    reviews = Review.objects.filter(video_game = v)

    return render_to_response('game_detail_page.html',
                             locals(),
                             context_instance=RequestContext(request))

def user_profile(request):
    title = "User Profile"

    try:
        profile = request.user.get_profile()
    except ObjectDoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            profile.gender = form.cleaned_data['gender']
            profile.location = form.cleaned_data['location']
            profile.date_of_birth = form.cleaned_data['date_of_birth']
            profile.about_you = form.cleaned_data['about_you']
            for p in form.cleaned_data['platforms_owned']:
                profile.platforms_owned.add(p)

            request.user.save()
            profile.save()

    else:
        form = UserProfileForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'gender': profile.gender,
            'location': profile.location,
            'date_of_birth': profile.date_of_birth,
            'about_you': profile.about_you,
            'platforms_owned': profile.platforms_owned
        })

    return render_to_response('user_profile.html',
                              locals(),
                              context_instance=RequestContext(request))
