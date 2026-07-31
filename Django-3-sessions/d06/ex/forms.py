from django import ModelForm

from .models import ModelTips


class TipsForm(ModelForm):
    class Meta:
        model = ModelTips
        fields = ("content", "author")
