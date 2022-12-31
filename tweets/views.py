from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from tweets.forms import TweetCreateForm
from tweets.models import Tweet, Favorite


class TweetHomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tweets = Tweet.objects.select_related("user").all()
        context = {"tweets": tweets}
        return render(request, "tweets/tweets_home.html", context)


class TweetCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = TweetCreateForm()
        return render(request, "tweets/tweets_create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = TweetCreateForm(data=request.POST)
        if form.is_valid():
            content = form.cleaned_data.get("content")
            Tweet.objects.create(user=request.user, content=content)
            return redirect("welcome:home")
        return render(request, "tweets/tweets_create.html", {"form": form})


class TweetDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tweet = get_object_or_404(
            Tweet,
            pk=kwargs.get("pk"),
        )
        if tweet.user != request.user:
            return HttpResponseForbidden()
        return render(request, "tweets/tweets_detail.html", {"tweet": tweet})


class TweetDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(
            Tweet,
            pk=kwargs.get("pk"),
        )
        if tweet.user != request.user:
            return HttpResponseForbidden()
        tweet.delete()
        return redirect("welcome:home")


class LikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(
            Tweet,
            pk=kwargs.get("pk"),
        )
        if Favorite.objects.filter(user=request.user, tweet=tweet).exists():
            return HttpResponse("Already liked", status=200)
        Favorite.objects.create(user=request.user, tweet=tweet)
        return HttpResponse("OK", status=200)


class UnlikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(
            Tweet,
            pk=kwargs.get("pk"),
        )
        if not Favorite.objects.filter(user=request.user, tweet=tweet).exists():
            return HttpResponse("Already liked", status=200)
        Favorite.objects.delete(user=request.user, tweet=tweet)
        return HttpResponse("OK", status=200)
