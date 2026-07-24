from django import forms

class BasicForm(forms.Form):
    text = forms.CharField(
        label="your text",
        max_length=200,
        widget=forms.TextInput(
            attrs= {'class': 'form-control', 'placeholder': 'Entrez du texte ici'}
            )
        )
