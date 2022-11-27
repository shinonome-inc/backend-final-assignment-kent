from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from tweets.forms import TweetCreateForm
from tweets.models import Tweet


class TweetHomeView(View):
    def get(self, request, *args, **kwargs):
        tweets = Tweet.objects.select_related("user").all()
        context = {"tweets": tweets}
        return render(request, "tweets/tweets_home.html", context)


class TweetCreateView(View):
    def get(self, request, *args, **kwargs):
        form = TweetCreateForm(request.POST)
        return render(request, "tweets/tweets_create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = TweetCreateForm(data=request.POST)
        if form.is_valid():
            content = form.cleaned_data.get("content")
            Tweet.objects.create(user=request.user, content=content)
            return redirect("welcome:home")
        return render(request, "tweets/tweets_create.html", {"form": form})


class TweetDetailView(View):
    def get(self, request, *args, **kwargs):
        tweet = get_object_or_404(
            Tweet,
            pk=kwargs.get("pk"),
        )
        if tweet.user != request.user:
            return HttpResponseForbidden()
        return render(request, "tweets/tweets_detail.html", {"tweet": tweet})


class TweetDeleteView(View):
    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(
            Tweet,
            pk=kwargs.get("pk"),
        )
        if tweet.user != request.user:
            return HttpResponseForbidden()
        else:
            tweet.delete()
        return redirect("welcome:home")
