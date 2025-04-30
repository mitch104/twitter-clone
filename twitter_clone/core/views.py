from typing import Any, cast

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView, View
from django.views.generic.base import ContextMixin

from .forms import (
    TweetForm,
    UserRegisterForm,
    UserUpdateForm,
)
from .models import CustomUser, Follow, Like, Tweet


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "core/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form: UserRegisterForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(self.request, f'Account created for {form.cleaned_data.get("username")}! You can now log in')
        return response


class TweetContextMixin(ContextMixin):
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["liked_tweets"] = self.request.user.likes.values_list("tweet_id", flat=True)
        context["retweeted_tweets"] = Tweet.objects.filter(parent__isnull=False, user=self.request.user).values_list(
            "parent_id", flat=True
        )
        return context


class HomeView(LoginRequiredMixin, TweetContextMixin, ListView):
    template_name = "core/home.html"
    model = Tweet
    context_object_name = "tweets"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Tweet]:
        following = Follow.objects.filter(follower=self.request.user).values_list("following", flat=True)
        return Tweet.objects.filter(Q(user__in=following) | Q(user=self.request.user)).order_by("-created_at")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["form"] = TweetForm()
        return context


class ExploreView(LoginRequiredMixin, TweetContextMixin, ListView):
    template_name = "core/explore.html"
    model = Tweet
    context_object_name = "tweets"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Tweet]:
        return Tweet.objects.all().order_by("-created_at")


class UsersListView(LoginRequiredMixin, ListView):
    template_name = "core/users_list.html"
    model = CustomUser
    context_object_name = "users"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[CustomUser]:
        return CustomUser.objects.exclude(id=self.request.user.id).order_by("username")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["following"] = self.request.user.following.values_list("following_id", flat=True)
        context["search_query"] = self.request.GET.get("search", "")
        return context


class TweetDetailView(LoginRequiredMixin, TweetContextMixin, DetailView):
    template_name = "core/tweet_detail.html"
    model = Tweet
    context_object_name = "tweet"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        tweet = cast(Tweet, self.object)
        context["retweets"] = Tweet.objects.filter(parent=tweet).order_by("-created_at")
        return context


class NewTweetView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TweetForm
    success_url = reverse_lazy("home")
    success_message = "Your tweet has been posted!"

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class LikeTweetView(LoginRequiredMixin, TweetContextMixin, DetailView):
    model = Tweet
    template_name = "core/tweet_card.html"
    slug_field = "id"
    slug_url_kwarg = "tweet_id"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        tweet = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
        if not created:
            like.delete()
        return super().get(request, *args, **kwargs)


class RetweetView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        original_tweet = get_object_or_404(Tweet, pk=kwargs["tweet_id"])
        retweet, created = Tweet.objects.get_or_create(
            user=request.user, content=original_tweet.content, parent=original_tweet, image=original_tweet.image
        )
        if not created:
            retweet.delete()
        return redirect(request.META.get("HTTP_REFERER", reverse_lazy("home")))


class ProfileView(LoginRequiredMixin, TweetContextMixin, DetailView):
    model = CustomUser
    template_name = "core/profile.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["is_following"] = self.object.is_followed_by(self.request.user)
        return context


class EditProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = "core/edit_profile.html"
    success_message = "Your profile has been updated successfully!"
    success_url = reverse_lazy("edit_profile")

    def get_object(self, queryset: QuerySet[CustomUser] | None = None) -> CustomUser:
        return cast(CustomUser, self.request.user)


class FollowUserView(LoginRequiredMixin, FormView):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user_to_follow = get_object_or_404(CustomUser, username=kwargs["username"])
        if user_to_follow == request.user:
            raise PermissionDenied("You cannot follow yourself.")

        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        if not created:
            follow.delete()

        return redirect(request.META.get("HTTP_REFERER", reverse_lazy("home")))
