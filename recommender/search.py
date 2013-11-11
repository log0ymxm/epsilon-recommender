from django import forms

class SearchForm(forms.Form):
    title = forms.CharField(max_length=100)
    releaseDate = forms.DateField()
    platform = forms.CharField(max_length=100)
    genre = forms.CharField(max_length=100)
