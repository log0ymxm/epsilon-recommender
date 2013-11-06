from django.contrib import admin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin

from recommender.models import VideoGame, Review, VideoGameAttribute, UserProfile

class VideoGameAttributeInlineForm(forms.ModelForm):
    pass

class VideoGameAttributeInline(admin.TabularInline):
    model = VideoGameAttribute
    extra = 2
    form = VideoGameAttributeInlineForm

class VideoGameAdmin(admin.ModelAdmin):
    inlines = [VideoGameAttributeInline]
    list_display= ('name', 'ign_url', 'description',)
    pass

class ReviewAdmin(admin.ModelAdmin):
    pass

class VideoGameAttributeAdmin(admin.ModelAdmin):
    raw_id_fields = ('video_game',)
    pass

class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(VideoGame, VideoGameAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(VideoGameAttribute, VideoGameAttributeAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
