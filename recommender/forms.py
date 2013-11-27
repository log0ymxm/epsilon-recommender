from django import forms
from recommender.models import Platform, Genre
from django_select2 import *
from recommender.widgets import CustomCheckboxSelectMultiple

class SearchForm(forms.Form):
    title = forms.CharField(max_length=100, required = False)
    release_date = forms.DateField(required = False)
    platform = ModelSelect2Field(queryset=Platform.objects, required=False)
    genre = ModelSelect2Field(queryset=Genre.objects, required=False)


class UserProfileForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    gender = forms.CharField(max_length=100, required=False)
    location = forms.CharField(max_length=100, required=False)
    date_of_birth = forms.DateField(required=False)
    about_you = forms.CharField(widget=forms.Textarea, required=False)
    platforms_owned = forms.ModelMultipleChoiceField(Platform.objects.all(),
                                                     required=False,
                                                     widget=CustomCheckboxSelectMultiple)

class ReviewForm(forms.Form):
    review = forms.CharField(widget=forms.Textarea)
