from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileUpdateForm, TweetForm, UserRegisterForm, UserUpdateForm
from .models import Follow, Like, Profile, Tweet


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})


@login_required
def home(request):
    following = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    tweets = Tweet.objects.filter(Q(user__in=following) | Q(user=request.user)).order_by('-created_at')
    
    # Get tweets liked by the user
    liked_tweets = []
    if request.user.is_authenticated:
        liked_tweets = Like.objects.filter(user=request.user).values_list('tweet_id', flat=True)
    
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            messages.success(request, 'Your tweet has been posted!')
            return redirect('home')
    else:
        form = TweetForm()
        
    context = {
        'tweets': tweets,
        'form': form,
        'liked_tweets': liked_tweets
    }
    return render(request, 'core/home.html', context)


def explore(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    
    # Get tweets liked by the user
    liked_tweets = []
    if request.user.is_authenticated:
        liked_tweets = Like.objects.filter(user=request.user).values_list('tweet_id', flat=True)
    
    return render(request, 'core/explore.html', {'tweets': tweets, 'liked_tweets': liked_tweets})


def users_list(request):
    # Get all users except the current user
    users = User.objects.exclude(id=request.user.id) if request.user.is_authenticated else User.objects.all()
    
    # Get the users followed by the current user
    following = []
    if request.user.is_authenticated:
        following = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    
    # Filter users by search query if provided
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) | 
            Q(email__icontains=search_query)
        )
    
    context = {
        'users': users,
        'following': following,
        'search_query': search_query
    }
    return render(request, 'core/users_list.html', context)


def tweet_detail(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    
    # Check if the user liked this tweet
    liked = False
    if request.user.is_authenticated:
        liked = Like.objects.filter(user=request.user, tweet=tweet).exists()
    
    return render(request, 'core/tweet_detail.html', {'tweet': tweet, 'liked': liked})


@login_required
def new_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            messages.success(request, 'Your tweet has been posted!')
            return redirect('home')
    else:
        form = TweetForm()
    return render(request, 'core/new_tweet.html', {'form': form})


@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
        
    # Get updated liked tweets list for the template
    liked_tweets = Like.objects.filter(user=request.user).values_list('tweet_id', flat=True)
    
    return render(request, 'core/tweet_card.html', {
        'tweet': tweet,
        'liked_tweets': liked_tweets,
        'retweeted_tweets': []  # Add this if you want to track retweets too
    })


@login_required
def retweet(request, tweet_id):
    original_tweet = get_object_or_404(Tweet, id=tweet_id)
    
    # Check if user already retweeted this tweet
    existing_retweet = Tweet.objects.filter(parent=original_tweet, user=request.user).first()
    
    if existing_retweet:
        existing_retweet.delete()
        retweeted = False
    else:
        retweet = Tweet(user=request.user, content=original_tweet.content, parent=original_tweet)
        if original_tweet.image:
            retweet.image = original_tweet.image
        retweet.save()
        retweeted = True
    
    # Get updated retweeted tweets list for the template
    retweeted_tweets = Tweet.objects.filter(
        parent=original_tweet,
        user=request.user
    ).values_list('parent_id', flat=True)
    
    return render(request, 'core/tweet_card.html', {
        'tweet': original_tweet,
        'liked_tweets': Like.objects.filter(user=request.user).values_list('tweet_id', flat=True),
        'retweeted_tweets': retweeted_tweets
    })


def profile(request, username):
    user = get_object_or_404(User, username=username)
    tweets = Tweet.objects.filter(user=user).order_by('-created_at')
    
    # Get tweets liked by the user
    liked_tweets = []
    if request.user.is_authenticated:
        liked_tweets = Like.objects.filter(user=request.user).values_list('tweet_id', flat=True)
    
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    
    context = {
        'profile_user': user,
        'tweets': tweets,
        'is_following': is_following,
        'liked_tweets': liked_tweets
    }
    return render(request, 'core/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'core/edit_profile.html', context)


@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    
    if user_to_follow == request.user:
        messages.warning(request, "You cannot follow yourself")
        return redirect('profile', username=username)
    
    follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    
    if not created:
        follow.delete()
        is_following = False
        messages.success(request, f'You unfollowed {username}')
    else:
        is_following = True
        messages.success(request, f'You are now following {username}')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'is_following': is_following,
            'followers_count': user_to_follow.profile.get_followers_count()
        })
    
    # Redirect back to the page that initiated the follow action
    referer = request.META.get('HTTP_REFERER')
    if referer and 'users' in referer:
        return redirect('users_list')
        
    return redirect('profile', username=username) 