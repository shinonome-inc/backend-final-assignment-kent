from django.urls import path
from .views import WelcomeView


app_name = "welcome"
urlpatterns = [
    path("", WelcomeView.as_view(), name="home"),
]
