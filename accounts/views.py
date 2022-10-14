from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from .forms import UserCreateForm


# アカウント作成
class SignUpView(UserCreateForm):
    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/")
        return render(
            request,
            "create.html",
            {
                "form": form,
            },
        )

    def get(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        return render(
            request,
            "create.html",
            {
                "form": form,
            },
        )
