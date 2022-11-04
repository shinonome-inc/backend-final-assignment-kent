from django.shortcuts import render

# Create your views here.
from django.views.generic import View


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        context = {"user": user}
        return render(request, "index.html", context)
