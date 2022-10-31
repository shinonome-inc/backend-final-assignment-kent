from colorama import Fore
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
from django.views.generic import View

from accounts.tests import print_colored_text


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        signin_url = reverse("accounts:signin")
        signout_url = reverse("accounts:signout")
        print_colored_text("signin_url", Fore.BLUE)
        print_colored_text(
            "------------------------------------------------------", Fore.BLUE
        )
        context = {"user": user, "signin_url": signin_url, "signout_url": signout_url}
        return render(request, "index.html", context)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        signin_url = reverse("accounts:signin")
        signout_url = reverse("accounts:signout")
        print_colored_text("signin_url", Fore.BLUE)
        print_colored_text(
            "------------------------------------------------------", Fore.BLUE
        )
        context = {"user": user, "signin_url": signin_url, "signout_url": signout_url}
        return render(request, "index.html", context)
