from typing import Any, TypeVar, cast

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
)

from .forms import (
    TweetForm,
    UserRegisterForm,
    UserUpdateForm,
)
from .models import CustomUser, Follow, Like, Tweet

_T = TypeVar('_T', bound=Any)


class RegisterView(FormView):
    template_name = 'core/register.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form: UserRegisterForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(self.request, f'Account created for {form.cleaned_data.get("username")}! You can now log in')
        return response


class HomeView(LoginRequiredMixin, ListView):
    template_name = 'core/home.html'
    model = Tweet
    context_object_name = 'tweets'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Tweet]:
        following = Follow.objects.filter(follower=self.request.user).values_list('following', flat=True)
        return Tweet.objects.filter(
            Q(user__in=following) | Q(user=self.request.user)
        ).order_by('-created_at')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['form'] = TweetForm()
        return context


class ExploreView(LoginRequiredMixin, ListView):
    template_name = 'core/explore.html'
    model = Tweet
    context_object_name = 'tweets'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Tweet]:
        return Tweet.objects.all().order_by('-created_at')


class UsersListView(LoginRequiredMixin, ListView):
    template_name = 'core/users_list.html'
    model = CustomUser
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[CustomUser]:
        return CustomUser.objects.exclude(id=self.request.user.id).order_by('username')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['following'] = Follow.objects.filter(
                follower=self.request.user
            ).values_list('following_id', flat=True)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class TweetDetailView(LoginRequiredMixin, DetailView):
    template_name = 'core/tweet_detail.html'
    model = Tweet
    context_object_name = 'tweet'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        tweet = cast(Tweet, self.object)
        context['replies'] = Tweet.objects.filter(parent=tweet).order_by('created_at')
        return context


class NewTweetView(LoginRequiredMixin, CreateView):
    template_name = 'core/new_tweet.html'
    form_class = TweetForm
    success_url = '/'

    def form_valid(self, form: TweetForm) -> HttpResponse:
        form.instance.user = self.request.user
        messages.success(self.request, 'Your tweet has been posted!')
        return super().form_valid(form)


class LikeTweetView(LoginRequiredMixin, FormView):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        tweet = get_object_or_404(Tweet, pk=kwargs['pk'])
        like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
        if not created:
            like.delete()
        return redirect('tweet_detail', pk=tweet.pk)


class RetweetView(LoginRequiredMixin, FormView):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        original_tweet = get_object_or_404(Tweet, pk=kwargs['pk'])
        retweet = Tweet.objects.create(
            user=request.user,
            content=original_tweet.content,
            parent=original_tweet
        )
        if original_tweet.image:
            retweet.image = original_tweet.image
            retweet.save()
        return redirect('tweet_detail', pk=retweet.pk)


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'core/profile.html'
    model = CustomUser
    context_object_name = 'user'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        user = cast(CustomUser, self.object)
        context['tweets'] = Tweet.objects.filter(user=user).order_by('-created_at')
        context['is_following'] = Follow.objects.filter(
            follower=self.request.user,
            following=user
        ).exists()
        return context


class EditProfileView(LoginRequiredMixin, FormView):
    template_name = 'core/edit_profile.html'
    form_class = UserUpdateForm
    success_url = '/'

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form: UserUpdateForm) -> HttpResponse:
        form.save()
        return super().form_valid(form)


class FollowUserView(LoginRequiredMixin, FormView):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user_to_follow = get_object_or_404(CustomUser, username=kwargs['username'])
        if user_to_follow == request.user:
            raise PermissionDenied("You cannot follow yourself.")

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        if not created:
            follow.delete()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(status=204)
        return redirect('profile', username=user_to_follow.username)
