from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View
from django.conf import settings

from .forms import UserCreateForm, UserSignInForm


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
            "signup.html",
            {
                "form": form,
            },
        )

    def get(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        return render(
            request,
            "signup.html",
            {
                "form": form,
            },
        )


class SignInView(View):
    LOGIN_REDIRECT_URL = getattr(settings, "LOGIN_REDIRECT_URL")

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
                return redirect(SignInView.LOGIN_REDIRECT_URL)
            else:
                return render(request, "signin.html", {"context": "ログインに失敗しました"})
        else:
            return render(request, "signin.html", {"context": "formが無効です"})

    def get(self, request, *args, **kwargs):
        template_name = "signin.html"
        form = UserSignInForm()
        return render(request, template_name, {"form": form})


class SignOutView(View):
    LOGOUT_REDIRECT_URL = getattr(settings, "LOGOUT_REDIRECT_URL")

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(SignOutView.LOGOUT_REDIRECT_URL)
