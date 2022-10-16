from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views.generic import View

from .forms import UserCreateForm
from .tests import TestSignUpView


class SignUpView(View):
    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            print(f"username:{username}")
            password = form.cleaned_data.get("password1")
            print(f"password:{password}")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/accounts/home")
        return render(
            request,
            "signup.html",
            {
                "form": form,
            },
        )

    def test_view():
        test = TestSignUpView()
        test.test_success_get()
        test.test_success_get()
        test.test_failure_post_with_empty_form()

    def get(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        SignUpView.test_view()
        return render(
            request,
            "signup.html",
            {
                "form": form,
            },
        )


class HomeView(View):
    def post(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        return render(request, "home.html")
