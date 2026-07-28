from django.forms import forms

from .models import People


from django import forms
from .models import People

class SearchCharMovieForm(forms.Form):
    Movies_minimum_release_date = forms.DateField(
        label="Movies minimum release date",
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    Movies_maximum_release_date = forms.DateField(
        label="Movies maximum release date",
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    Planet_diameter_greater_than = forms.IntegerField(
        label="Planet diameter greater than",
        required=True
    )
    
    Character_gender = forms.ChoiceField(
        required=True,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
        ],
    )