from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import Unauthorized
from tastypie.authentication import Authentication
from tastypie.http import HttpUnauthorized, HttpForbidden

from recommender.models import *
from django.contrib.auth.models import User

class EmailApiKeyAuthentication(Authentication):
    def _unauthorized(self):
        return HttpUnauthorized()

    def extract_credentials(self, request):
        if request.META.get('HTTP_AUTHORIZATION') and request.META['HTTP_AUTHORIZATION'].lower().startswith('apikey '):
            (auth_type, data) = request.META['HTTP_AUTHORIZATION'].split()

            if auth_type.lower() != 'apikey':
                raise ValueError("Incorrect authorization header.")

            api_key = data
        else:
            api_key = request.GET.get('api_key') or request.POST.get('api_key')

        return api_key

    def is_authenticated(self, request, **kwargs):
        """
        Finds the user and checks their API key.

        Should return either ``True`` if allowed, ``False`` if not or an
        ``HttpResponse`` if you need something custom.
        """

        try:
            api_key = self.extract_credentials(request)
        except ValueError:
            return self._unauthorized()

        if not api_key:
            return self._unauthorized()

        (user, key_auth_check) = self.get_key(api_key)

        if not self.check_active(user):
            return False

        if key_auth_check and not isinstance(key_auth_check, HttpUnauthorized):
            request.user = user

        return key_auth_check

    def get_key(self, api_key):
        """
        Attempts to find the API key for the user. Uses ``ApiKey`` by default
        but can be overridden.
        """
        from tastypie.models import ApiKey

        try:
            key = ApiKey.objects.get(key=api_key)
        except ApiKey.DoesNotExist:
            return (null, self._unauthorized())

        return (key.user, True)

    def get_identifier(self, request):
        """
        Provides a unique string identifier for the requestor.

        This implementation returns the user's email.
        """
        return request.user or 'nouser'

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        serializer = Serializer(formats=['jsonp', 'json'])
        authorization = DjangoAuthorization()
        authentication = EmailApiKeyAuthentication()
        trailing_slash = False
        fields = ['id', 'username']

class VideoGameResource(ModelResource):
    class Meta:
        queryset = VideoGame.ranked.all()
        filtering = {
            'name': ('exact'),
            'description': ('exact'),
            }
        resource_name = 'video_game'
        serializer = Serializer(formats=['jsonp', 'json'])
        authorization = DjangoAuthorization()
        authentication = EmailApiKeyAuthentication()
        trailing_slash = False
        fields = ['name', 'description',]

class ReviewResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True, null=True, blank=True)
    video_game = fields.ForeignKey(VideoGameResource, 'video_game', full=True, null=True, blank=True)
    # TODO rating fields

    class Meta:
        queryset = Review.objects.all()
        filtering = {
            'comments': ('exact'),
            }
        resource_name = 'review'
        serializer = Serializer(formats=['jsonp', 'json'])
        authorization = DjangoAuthorization()
        authentication = EmailApiKeyAuthentication()
        trailing_slash = False
        fields = ['comments',]

class FeatureResource(ModelResource):
    class Meta:
        queryset = Feature.objects.all()
        filtering = {}
        resource_name = 'feature'
        serializer = Serializer(formats=['jsonp', 'json'])
        authorization = DjangoAuthorization()
        authentication = EmailApiKeyAuthentication()
        trailing_slash = False
        fields = ['name',]

class PlatformResource(ModelResource):
    class Meta:
        queryset = Platform.objects.all()
        filtering = {}
        resource_name = 'platform'
        serializer = Serializer(formats=['jsonp', 'json'])
        authorization = DjangoAuthorization()
        authentication = EmailApiKeyAuthentication()
        trailing_slash = False
        fields = ['name',]

class SpecificationResource(ModelResource):
    class Meta:
        queryset = Specification.objects.all()
        filtering = {}
        resource_name = 'specification'
        serializer = Serializer(formats=['jsonp', 'json'])
        authorization = DjangoAuthorization()
        authentication = EmailApiKeyAuthentication()
        trailing_slash = False
        fields = ['name',]
