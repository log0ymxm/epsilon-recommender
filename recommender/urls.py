from django.conf.urls import patterns, include, url
from tastypie.api import Api
from recommender.api import UserResource, VideoGameResource, ReviewResource
from recommender import settings
from djangoratings.views import AddRatingFromModel

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(VideoGameResource())
v1_api.register(ReviewResource())

rating_config = {
    'app_label': 'recommender',
    'model': 'videogame',
    'field_name': 'rating',
}

urlpatterns = patterns('',
                       url(r'^$', 'recommender.views.home', name='home'),
                       url(r'^accounts/', include('registration.backends.default.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^api/', include(v1_api.urls)),
                       url(r'^games/(?P<slug>[\w-]+)$', 'recommender.views.game_detail_page', name='game_detail_page'),
                       url(r'^genre$', 'recommender.views.genre_detail', name='genre'),
                       url(r'^genre/(?P<slug>[\w-]+)/$', 'recommender.views.genre_detail', name='genre'),
                       url(r'^profile', 'recommender.views.user_profile', name='user_profile'),
                       url(r'^recommendations$', 'recommender.views.recommendations', name='recommendations'),
                       url(r'^search$', 'recommender.views.search', name='search'),
                       url(r'^select2/', include('django_select2.urls')),
                       url(r'rate/(?P<object_id>\d+)/(?P<score>\d+)', AddRatingFromModel(), rating_config),
)

if settings.PRODUCTION:
    urlpatterns += patterns('',
                            url(r'^static/(?P<path>.*)$', 'django.contrib.staticfiles.views.serve',
                                {'document_root': settings.STATIC_ROOT}),
    )
