from django.conf.urls import patterns, include, url
from tastypie.api import Api
from recommender.api import UserResource, VideoGameResource, ReviewResource, AttributeOptionResource, VideoGameAttributeResource
from recommender import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(VideoGameResource())
v1_api.register(ReviewResource())
v1_api.register(AttributeOptionResource())
v1_api.register(VideoGameAttributeResource())

urlpatterns = patterns('',

    url(r'^$', 'recommender.views.home', name='home'),
    url(r'^recommendations$', 'recommender.views.recommendations', name='recommendations'),
    url(r'^search_and_rate$', 'recommender.views.search_and_rate', name='search_and_rate'),
    url(r'^game-detail-page$', 'recommender.views.game_detail_page', name='game_detail_page'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
)

if settings.PRODUCTION:
    urlpatterns += patterns('',
                            url(r'^static/(?P<path>.*)$', 'django.contrib.staticfiles.views.serve',
                                {'document_root': settings.STATIC_ROOT}),
                            )
