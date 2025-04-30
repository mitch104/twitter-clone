import pytest
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse

from apps.core.models import Tweet
from tests.factories import LikeFactory, TweetFactory


@pytest.mark.django_db()
class TestLikeTweetView:
    def test_like_tweet__creates_like(self, logged_in_client: Client, tweet: Tweet) -> None:
        response: HttpResponse = logged_in_client.get(reverse("like_tweet", kwargs={"tweet_id": tweet.id}))

        assert response.status_code == 200
        assert tweet.likes.filter(user=logged_in_client.user).exists()
        assert response.context["tweet"] == tweet
        assert tweet.id in response.context["liked_tweets"]

    def test_like_tweet__removes_existing_like(self, logged_in_client: Client, tweet: Tweet) -> None:
        LikeFactory(user=logged_in_client.user, tweet=tweet)

        response: HttpResponse = logged_in_client.get(reverse("like_tweet", kwargs={"tweet_id": tweet.id}))

        assert response.status_code == 200
        assert not tweet.likes.filter(user=logged_in_client.user).exists()
        assert response.context["tweet"] == tweet
        assert tweet.id not in response.context["liked_tweets"]


@pytest.mark.django_db()
class TestRetweetView:
    def test_retweet__creates_retweet(self, logged_in_client: Client, tweet: Tweet) -> None:
        url = reverse("retweet", kwargs={"tweet_id": tweet.id})
        response: HttpResponse = logged_in_client.post(url)

        assert response.status_code == 302
        # Check that a retweet was created
        retweet = Tweet.objects.filter(parent=tweet, user=logged_in_client.user).first()
        assert retweet is not None
        assert tweet.get_retweets_count() == 1

    def test_retweet__removes_existing_retweet(self, logged_in_client: Client, tweet: Tweet) -> None:
        # Create an existing retweet
        TweetFactory(user=logged_in_client.user, parent=tweet)

        response: HttpResponse = logged_in_client.post(reverse("retweet", kwargs={"tweet_id": tweet.id}))

        assert response.status_code == 302
        # Check that the retweet was removed
        assert not Tweet.objects.filter(parent=tweet, user=logged_in_client.user).exists()
        assert tweet.get_retweets_count() == 0


@pytest.mark.django_db()
class TestNewTweetView:
    def test_post_new_tweet(self, logged_in_client: Client) -> None:
        tweet_text = "This is a test tweet!"
        response: HttpResponse = logged_in_client.post(reverse("new_tweet"), {"content": tweet_text})

        assert response.status_code == 302
        assert Tweet.objects.filter(content=tweet_text, user=logged_in_client.user).exists()
