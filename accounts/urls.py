from django.urls import path

from accounts import views

app_name = "accounts"
urlpatterns = [
    path("signup", views.SignUpView.as_view(), name="signup"),
    path("signin", views.SignInView.as_view(), name="signin"),
    path("signout", views.SignOutView.as_view(), name="signout"),
    path("<str:username>/profile/", views.UserProfileView.as_view(), name="profile"),
    path(
        "<str:username>/profile/edit/",
        views.UserProfileEditView.as_view(),
        name="profile_edit",
    ),
    # path(
    #    "<str:username>/following_list/",
    #    views.FollowingListView.as_view(),
    #    name="following_list",
    # ),
    # path(
    #    "<str:username>/follower_list/",
    #    views.FollowerListView.as_view(),
    #    name="follower_list",
    # ),
    path("<str:username>/follow/", views.FollowView.as_view(), name="follow"),
    path("<str:username>/unfollow/", views.UnFollowView.as_view(), name="unfollow"),
]
