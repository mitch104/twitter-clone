import pytest
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse

from apps.core.models import Tweet
from tests.factories import LikeFactory


@pytest.mark.django_db()
class TestLikeTweetView:
    def test_like_tweet__creates_like(self, logged_in_client: Client, tweet: Tweet) -> None:
        url = reverse("like_tweet", kwargs={"tweet_id": tweet.id})
        response: HttpResponse = logged_in_client.get(url)

        assert response.status_code == 200
        assert tweet.likes.filter(user=logged_in_client.user).exists()
        assert response.context["tweet"] == tweet
        assert tweet.id in response.context["liked_tweets"]

    def test_like_tweet__removes_existing_like(self, logged_in_client: Client, tweet: Tweet) -> None:
        LikeFactory(user=logged_in_client.user, tweet=tweet)
        assert tweet.likes.filter(user=logged_in_client.user).exists()

        url = reverse("like_tweet", kwargs={"tweet_id": tweet.id})
        response: HttpResponse = logged_in_client.get(url)

        assert response.status_code == 200
        assert not tweet.likes.filter(user=logged_in_client.user).exists()
        assert response.context["tweet"] == tweet
        assert tweet.id not in response.context["liked_tweets"]
