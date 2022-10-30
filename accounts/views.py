from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View

from .forms import SignInForm, UserCreateForm


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


class SignInView(LoginView):
    template_name = "signin.html"
    form_class = SignInForm


class SignOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse("welcome:home"))

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse("welcome:home"))
