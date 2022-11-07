from django import forms

from tweets.models import Tweet


class TweetCreateForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ("content",)
