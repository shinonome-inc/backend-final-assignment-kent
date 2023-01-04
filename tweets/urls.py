from django.urls import path

from . import views

app_name = "tweets"
urlpatterns = [
    path("home/", views.TweetHomeView.as_view(), name="home"),
    path("create/", views.TweetCreateView.as_view(), name="create"),
    path("<int:pk>/detail", views.TweetDetailView.as_view(), name="detail"),
    path("<int:pk>/delete/", views.TweetDeleteView.as_view(), name="delete"),
    path("<int:pk>/favorite/", views.FavoriteView.as_view(), name="favorite"),
    path("<int:pk>/unfavorite/", views.UnfavoriteView.as_view(), name="unfavorite"),
]
