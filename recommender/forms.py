from django import forms

class SearchForm(forms.Form):
    title = forms.CharField(max_length=100, required = False)
    releaseDate = forms.DateField(required = False)
    platform = forms.CharField(max_length=100,required = False)
    genre = forms.CharField(max_length=100, required = False)
    