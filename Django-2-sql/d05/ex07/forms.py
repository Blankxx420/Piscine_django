from django import forms
from .models import Movies


class Update_form(forms.Form):
    movie = forms.ModelChoiceField(
           queryset=Movies.objects.all(),
           to_field_name="episode_nb",  
           empty_label="-- Select a movie --",
           label="Choose a movie to update"
       )
    opening_crawl = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        required=False,
        label="Opening crawl"
    )