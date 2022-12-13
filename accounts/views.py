from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View

from accounts.forms import UserCreateForm, UserSignInForm
from accounts.models import FriendShip, User


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
                    {"context": "ログインに失敗しました", "error_occured": False},
                )
        else:
            return render(
                request,
                "accounts/signin.html",
                {"context": "formが無効です", "error_occured": True},
            )

    def get(self, request, *args, **kwargs):
        template_name = "accounts/signin.html"
        form = UserSignInForm()
        return render(request, template_name, {"form": form})


class SignOutView(LogoutView):
    pass


class UserProfileView(View):
    def get(self, request, *args, **kwargs):
        username = kwargs.get("username")
        requested_user = User.objects.get(username=username)
        follower_frindship_records = FriendShip.objects.filter(followee=requested_user)
        followee_friendship_records = FriendShip.objects.filter(follower=requested_user)
        follower_users = [
            follower_record.followee for follower_record in follower_frindship_records
        ]
        followee_users = [
            followee_record.follower for followee_record in followee_friendship_records
        ]
        context = {"followers": follower_users, "followees": followee_users}
        return render(request, "accounts/userprofile.html", context)


class UserProfileEditView(View):
    def post(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        pass


class FollowView(View):
    def post(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        pass


class UnfollowView(View):
    def post(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        pass


class FollowingListView(View):
    def post(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        pass


class FollowerListView(View):
    def post(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        pass


class UnFollowView(View):
    def post(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        pass
