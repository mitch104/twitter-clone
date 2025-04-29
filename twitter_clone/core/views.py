from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
    View,
)

from .forms import (
    ProfileUpdateForm,
    TweetForm,
    UserProfileUpdateForm,
    UserRegisterForm,
    UserUpdateForm,
)
from .models import Follow, Like, Tweet


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'core/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Account created for {form.cleaned_data.get("username")}! You can now log in')
        return response


class HomeView(LoginRequiredMixin, FormView):
    template_name = 'core/home.html'
    form_class = TweetForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        following = Follow.objects.filter(follower=self.request.user).values_list('following', flat=True)
        context['tweets'] = Tweet.objects.filter(
            Q(user__in=following) | Q(user=self.request.user)
        ).order_by('-created_at')
        context['liked_tweets'] = Like.objects.filter(
            user=self.request.user
        ).values_list('tweet_id', flat=True)
        return context

    def form_valid(self, form):
        tweet = form.save(commit=False)
        tweet.user = self.request.user
        tweet.save()
        messages.success(self.request, 'Your tweet has been posted!')
        return super().form_valid(form)


class ExploreView(ListView):
    template_name = 'core/explore.html'
    context_object_name = 'tweets'
    model = Tweet
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['liked_tweets'] = Like.objects.filter(
                user=self.request.user
            ).values_list('tweet_id', flat=True)
        return context


class UsersListView(ListView):
    template_name = 'core/users_list.html'
    context_object_name = 'users'
    model = User

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.exclude(id=self.request.user.id)
        
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query) | 
                Q(email__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['following'] = Follow.objects.filter(
                follower=self.request.user
            ).values_list('following_id', flat=True)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class TweetDetailView(DetailView):
    template_name = 'core/tweet_detail.html'
    model = Tweet
    context_object_name = 'tweet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['liked'] = Like.objects.filter(
                user=self.request.user,
                tweet=self.object
            ).exists()
        return context


class NewTweetView(LoginRequiredMixin, CreateView):
    template_name = 'core/new_tweet.html'
    form_class = TweetForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Your tweet has been posted!')
        return super().form_valid(form)


class LikeTweetView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tweet = get_object_or_404(Tweet, id=kwargs['tweet_id'])
        like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
        
        if not created:
            like.delete()
        
        liked_tweets = Like.objects.filter(user=request.user).values_list('tweet_id', flat=True)
        
        if request.htmx:
            return render(request, 'core/tweet_card.html', {
                'tweet': tweet,
                'liked_tweets': liked_tweets,
                'retweeted_tweets': []
            })
        
        return JsonResponse({
            'liked': created,
            'likes_count': tweet.get_likes_count()
        })


class RetweetView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        original_tweet = get_object_or_404(Tweet, id=kwargs['tweet_id'])
        existing_retweet = Tweet.objects.filter(
            parent=original_tweet,
            user=request.user
        ).first()
        
        if existing_retweet:
            existing_retweet.delete()
        else:
            retweet = Tweet(
                user=request.user,
                content=original_tweet.content,
                parent=original_tweet
            )
            if original_tweet.image:
                retweet.image = original_tweet.image
            retweet.save()
        
        retweeted_tweets = Tweet.objects.filter(
            parent=original_tweet,
            user=request.user
        ).values_list('parent_id', flat=True)
        
        if request.htmx:
            return render(request, 'core/tweet_card.html', {
                'tweet': original_tweet,
                'liked_tweets': Like.objects.filter(user=request.user).values_list('tweet_id', flat=True),
                'retweeted_tweets': retweeted_tweets
            })
        
        return JsonResponse({
            'retweeted': not existing_retweet,
            'retweets_count': original_tweet.get_retweets_count()
        })


class ProfileView(DetailView):
    template_name = 'core/profile.html'
    model = User
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tweets'] = Tweet.objects.filter(
            user=self.object
        ).order_by('-created_at')
        
        if self.request.user.is_authenticated:
            context['liked_tweets'] = Like.objects.filter(
                user=self.request.user
            ).values_list('tweet_id', flat=True)
            context['is_following'] = Follow.objects.filter(
                follower=self.request.user,
                following=self.object
            ).exists()
        
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'core/edit_profile.html'
    form_class = UserProfileUpdateForm
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})


class FollowUserView(LoginRequiredMixin, View):
    def post(self, request, username):
        profile_user = get_object_or_404(User, username=username)
        
        if request.user == profile_user:
            return HttpResponseForbidden("You cannot follow yourself")
        
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=profile_user
        )
        
        if not created:
            follow.delete()
            messages.success(request, f'You unfollowed {username}')
        else:
            messages.success(request, f'You are now following {username}')
        
        if referer := request.META.get('HTTP_REFERER'):
            return redirect(referer, username=username)
        return redirect('users_list')