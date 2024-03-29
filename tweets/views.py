from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from tweets.forms import TweetCreateForm
from tweets.models import Favorite, Tweet


class TweetHomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tweets = Tweet.objects.select_related("user").all()
        favorited_tweets = [
            favorite_record.tweet
            for favorite_record in Favorite.objects.filter(user=request.user)
        ]
        context = {
            "tweets": tweets,
            "favorited_tweets": favorited_tweets,
        }
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
        is_tweet_user = tweet.user == request.user
        favorite_count = Favorite.objects.filter(tweet=tweet).count()
        context = {
            "tweet": tweet,
            "favorite_count": favorite_count,
            "is_tweet_user": is_tweet_user,
        }
        return render(
            request,
            "tweets/tweets_detail.html",
            context,
        )


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


class FavoriteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(
            Tweet,
            pk=kwargs.get("pk"),
        )
        if Favorite.objects.filter(user=request.user, tweet=tweet).exists():
            return HttpResponse("UNIQUE constraint failed", status=200)
        Favorite.objects.create(user=request.user, tweet=tweet)
        params = {"tweet": tweet.id}
        return JsonResponse(params, status=200)


class UnfavoriteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(
            Tweet,
            pk=kwargs.get("pk"),
        )
        if not (
            favorite_record := Favorite.objects.filter(user=request.user, tweet=tweet)
        ):
            return HttpResponse("Favorite Record Unexist", status=200)
        favorite_record.delete()
        params = {"data": tweet.id}
        return JsonResponse(params, status=200)
