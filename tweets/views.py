from django.shortcuts import HttpResponse, render, redirect
from django.views.generic import View

from tweets.forms import TweetForm
from tweets.models import Tweet


class TweetCreateView(View):
    def get(self, request, *args, **kwargs):
        form = TweetForm(request.POST)
        return render(request, "tweets/tweets_create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = TweetForm(data=request.POST)
        if form.is_valid():
            content = form.cleaned_data.get("content")
            Tweet.objects.create(user=request.user, content=content)
            return redirect("welcome:home")
        return render(request, "tweets/tweets_create.html", {"form": form})


class TweetDetailView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("GET request!")

    def post(self, request, *args, **kwargs):
        return HttpResponse("POST request!")
