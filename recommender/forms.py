from django import forms
from recommender.models import Platform
from django_select2 import *

class SearchForm(forms.Form):
    title = forms.CharField(max_length=100, required = False)
    release_date = forms.DateField(required = False)
    platform = ModelSelect2MultipleField(queryset=Platform.objects, required=False)
    genre = forms.CharField(max_length=100, required = False)

   # def clean(self):
    #	cleaned_data = super(SearchForm, self).clean
    #	title = cleaned_data.get('title')
    #	releaseDate = cleaned_data.get('releaseDate')
    #	platform = cleaned_data.get('platform')
    #	genre = cleaned_data.get('genre')
