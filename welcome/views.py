from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from tweets.models import Tweet


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        user = self.request.user if self.request.user.is_authenticated else None
        tweets = Tweet.objects.select_related("user").all()
        context = {"user": user, "tweets": tweets}
        return render(request, "index.html", context)
