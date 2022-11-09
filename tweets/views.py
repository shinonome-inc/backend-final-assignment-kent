from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from tweets.forms import TweetCreateForm
from tweets.models import Tweet


class TweetCreateView(View):
    def get(self, request, *args, **kwargs):
        form = TweetCreateForm(request.POST)
        return render(request, "tweets_create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = TweetCreateForm(data=request.POST)
        if form.is_valid():
            content = form.cleaned_data.get("content")
            Tweet.objects.create(user=request.user, content=content)
            return redirect("welcome:home")
        return render(request, "tweets_create.html", {"form": form})


class TweetDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        return render(request, "tweets_detail.html", {"tweet": tweet})


class TweetDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        tweet.delete()
        return redirect("welcome:home")
