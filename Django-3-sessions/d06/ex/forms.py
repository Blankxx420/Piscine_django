from django import forms
from django.forms import ModelForm

from .models import ModelTips


class TipsForm(ModelForm):
    class Meta:
        model = ModelTips
        fields = ("content",)
        labels = {
            "content": "",
        }
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Write your tips here...",
                "rows": 6
            })
        }