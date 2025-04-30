import pytest
from django.test import Client

from apps.core.models import CustomUser, Tweet
from tests.factories import CustomUserFactory, TweetFactory


@pytest.fixture
def user() -> CustomUser:
    return CustomUserFactory()


@pytest.fixture
def logged_in_client(user: CustomUser, client: Client) -> Client:
    """Return a Django test client with a logged-in user."""
    client.force_login(user)
    client.user = user
    return client


@pytest.fixture
def tweet(user: CustomUser) -> Tweet:
    """Create a test tweet by the test user."""
    return TweetFactory(user=user)
