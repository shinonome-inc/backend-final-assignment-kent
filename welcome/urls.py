from django.urls import path

from welcome import views

app_name = "welcome"
urlpatterns = [
    path("", views.WelcomeHomeView.as_view(), name="home"),
]
