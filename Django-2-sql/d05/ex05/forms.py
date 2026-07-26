from django import forms

from .models import Movies


class DeleteMovieForm(forms.Form):

    movie = forms.ModelChoiceField(
        queryset=Movies.objects.all(),
        to_field_name="episode_nb",  
        empty_label="-- Select a movie --",
        label="Choose a movie to erase"
    )