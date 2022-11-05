from django.shortcuts import render, HttpResponse
from django.views.generic import View


# Create your views here.
class TweetCreateView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("GET request!")

    def post(self, request, *args, **kwargs):
        return HttpResponse("POST request!")


class TweetDetailView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("GET request!")

    def post(self, request, *args, **kwargs):
        return HttpResponse("POST request!")
