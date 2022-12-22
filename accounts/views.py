from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.forms import UserCreateForm, UserSignInForm
from accounts.models import FriendShip
from tweets.models import Tweet

User = get_user_model()


class SignUpView(View):
    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            email = form.cleaned_data.get("email")
            user = authenticate(username=username, email=email, password=password)
            login(request, user)
            return redirect(reverse("welcome:home"))
        return render(
            request,
            "accounts/signup.html",
            {
                "form": form,
            },
        )

    def get(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        return render(
            request,
            "accounts/signup.html",
            {
                "form": form,
            },
        )


class SignInView(View):
    def post(self, request, *args, **kwargs):
        form = UserSignInForm(data=request.POST)
        if form.is_valid():
            # フォームから'username'を読み取る
            username = form.cleaned_data.get("username")
            # フォームから'password'を読み取る
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                # 認証処理
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                return render(
                    request,
                    "signin.html",
                    {"context": "ログインに失敗しました", "error_occured": True},
                )
        else:
            return render(
                request,
                "accounts/signin.html",
                {"error_occured": True},
            )

    def get(self, request, *args, **kwargs):
        template_name = "accounts/signin.html"
        form = UserSignInForm()
        return render(request, template_name, {"form": form})


class SignOutView(LoginRequiredMixin, LogoutView):
    pass


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        requested_user = get_object_or_404(User, username=kwargs.get("username"))
        requested_username = requested_user.get_username()
        user_tweets = Tweet.objects.filter(user=requested_user)
        follower_count = FriendShip.objects.filter(followee=requested_user).count()
        followee_count = FriendShip.objects.filter(follower=requested_user).count()
        context = {
            "follower_count": follower_count,
            "followee_count": followee_count,
            "user_tweets": user_tweets,
            "requested_username": requested_username,
        }
        return render(request, "accounts/userprofile.html", context)


# class UserProfileEditView(View):
#    def post(self, request, *args, **kwargs):
#        pass
#
#    def get(self, request, *args, **kwargs):
#        pass


class FollowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        followee_record = get_object_or_404(User, username=kwargs.get("username"))
        follower_record = request.user
        if followee_record == request.user:
            response = HttpResponse(b"You can't follow yourself.")
            return response
        FriendShip.objects.create(follower=follower_record, followee=followee_record)
        return redirect(reverse("welcome:home"))


class UnfollowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        followee_record = get_object_or_404(User, username=kwargs.get("username"))
        follower_record = request.user
        if followee_record == request.user:
            response = HttpResponse(b"You can't follow yourself.")
            return response
        friendship_record = FriendShip.objects.get(
            follower=follower_record, followee=followee_record
        )
        friendship_record.delete()
        return redirect(reverse("welcome:home"))


class FollowerListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        frienships = FriendShip.objects.filter(followee=request.user)
        followers = [friendship.follower for friendship in frienships]
        return render(
            request,
            "accounts/followee_list.html",
            {
                "followers": followers,
            },
        )


class FolloweeListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        friendships = FriendShip.objects.filter(follower=request.user)
        followees = [friendship.follower for friendship in friendships]
        return render(
            request,
            "accounts/followee_list.html",
            {
                "followees": followees,
            },
        )
