from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from tweets.models import Tweet


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        tweets = Tweet.objects.filter(user=user).all()
        context = {"user": user, "tweets": tweets}
        return render(request, "index.html", context)
