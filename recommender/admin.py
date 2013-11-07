from django.contrib import admin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin

from recommender.models import *

class VideoGameAdmin(admin.ModelAdmin):
    list_display= ('name', 'ign_image', 'ign_url', 'description',)
    raw_id_fields = ('ign_games_you_may_like', 'specifications', 'features',)
    pass

class ReviewAdmin(admin.ModelAdmin):
    pass

class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(VideoGame, VideoGameAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Feature)
admin.site.register(Platform)
admin.site.register(Specification)
