from django.contrib import admin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin

from recommender.auth import CustomUser
from recommender.models import VideoGame, Review, VideoGameAttribute

class CustomUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(help_text="Raw passwords are not stored, so there is no way to see " +
                                         "this user's password, but you can change the password " +
                                         "using <a href=\"password/\">this form</a>.")

    class Meta:
        model = CustomUser

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'is_active', 'is_admin', 'last_login')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

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

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(VideoGame, VideoGameAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(VideoGameAttribute, VideoGameAttributeAdmin)
