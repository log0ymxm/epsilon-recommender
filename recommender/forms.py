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
    CHOICES = ((0,'Xbox 360'),(1,'Wii'),(2,'PS3'),(3,'Xbox One'), (4,'PS4'), (5,'Wii U'),(6,'3DS'), (7,'PC'),(8,'PSP'),(9,'PS Vita')) 
    #gravatar =
    name = forms.CharField(max_length=100, required = False)
    gender = forms.CharField(max_length=100, required = False)
    location = forms.CharField(max_length=100, required = False)
    date_of_birth = forms.DateField(required = False)
    about_you = forms.CharField(widget=forms.Textarea)
    platforms_owned = forms.MultipleChoiceField(required=False,
        widget=CustomCheckboxSelectMultiple, choices=CHOICES)

class ReviewForm(forms.Form):
    review = forms.CharField(widget=forms.Textarea)
    