from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("explore/", views.ExploreView.as_view(), name="explore"),
    path("users/", views.UsersListView.as_view(), name="users_list"),
    path("tweet/<int:pk>/", views.TweetDetailView.as_view(), name="tweet_detail"),
    path("tweet/new/", views.NewTweetView.as_view(), name="new_tweet"),
    path("tweet/<int:tweet_id>/like/", views.LikeTweetView.as_view(), name="like_tweet"),
    path("tweet/<int:tweet_id>/retweet/", views.RetweetView.as_view(), name="retweet"),
    path("profile/<str:username>/", views.ProfileView.as_view(), name="profile"),
    path("profile/<str:username>/follow/", views.FollowUserView.as_view(), name="follow_user"),
    path("edit_profile/", views.EditProfileView.as_view(), name="edit_profile"),
    path("register/", views.RegisterView.as_view(), name="register"),
]
