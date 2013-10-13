from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import Unauthorized

from attributes.models import AttributeOption
from recommender.models import VideoGame, Review, VideoGameAttribute
from recommender.auth import CustomUser

class UserResource(ModelResource):
    class Meta:
        queryset = CustomUser.objects.all()
        resource_name = 'user'
        serializer = Serializer(formats=['jsonp', 'json'])
        authorization = DjangoAuthorization()
        authentication = EmailApiKeyAuthentication()
        trailing_slash = False
        fields = ['id', 'name', 'email']

class VideoGameResource(ModelResource):
    class Meta:
        queryset = VideoGame.objects.all()
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

class AttributeOptionResource(ModelResource):
    class Meta:
        queryset = AttributeOption.objects.all()
        filtering = {
            'description': ('exact'),
            'name': ('exact'),
            }
        resource_name = 'attribute_option'
        serializer = Serializer(formats=['jsonp', 'json'])
        authorization = DjangoAuthorization()
        authentication = EmailApiKeyAuthentication()
        trailing_slash = False
        fields = ['description', 'name', 'validation', 'sort_order', 'error_message',]

class VideoGameAttributeResource(ModelResource):
    video_game = fields.ForeignKey(VideoGameResource, 'video_game', full=True, null=True, blank=True)
    option = fields.ForeignKey(AttributeOptionResource, 'option', full=True, null=True, blank=True)

    class Meta:
        queryset = VideoGameAttribute.objects.all()
        filtering = {
            'value': ('exact'),
            }
        resource_name = 'video_game_attribute'
        serializer = Serializer(formats=['jsonp', 'json'])
        authorization = DjangoAuthorization()
        authentication = EmailApiKeyAuthentication()
        trailing_slash = False
        fields = ['value',]
