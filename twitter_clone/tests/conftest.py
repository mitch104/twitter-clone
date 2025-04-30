import pytest
from django.test import Client

from twitter_clone.core.models import CustomUser, Tweet
from twitter_clone.tests.factories import TweetFactory, UserFactory


@pytest.fixture
def user() -> CustomUser:
    return UserFactory()


@pytest.fixture
def logged_in_client(user: CustomUser, client: Client) -> Client:
    client.force_login(user)
    return client


@pytest.fixture
def tweet(user: CustomUser) -> Tweet:
    return TweetFactory(user=user)
