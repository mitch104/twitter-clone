import pytest
from playwright.sync_api import Page, expect
from pytest_django.live_server_helper import LiveServer

from apps.core.models import CustomUser, Tweet
from tests.factories import CustomUserFactory


@pytest.fixture
def logged_in_page(live_server: LiveServer, page: Page, user: CustomUser) -> Page:
    """Fixture to handle user login."""
    page.goto(f"{live_server.url}/login/")
    page.fill("input[name='username']", user.username)
    page.fill("input[name='password']", "testpass123")
    page.click("button[type='submit']")
    expect(page).to_have_url(f"{live_server.url}/")
    return page


@pytest.mark.django_db(transaction=True)
class TestAuthentication:
    def test_failed_login(self, live_server: LiveServer, logged_in_page: Page) -> None:
        # Visit the login page
        logged_in_page.goto(f"{live_server.url}/login/")

        # Fill in login form with wrong credentials
        logged_in_page.fill("input[name='username']", "wronguser")
        logged_in_page.fill("input[name='password']", "wrongpass")
        logged_in_page.click("button[type='submit']")

        # Should stay on login page with error
        expect(logged_in_page).to_have_url(f"{live_server.url}/login/")
        expect(logged_in_page.get_by_text("Please enter a correct username and password")).to_be_visible()


@pytest.mark.django_db(transaction=True)
class TestTweetInteractions:
    def test_login_and_post_tweet(self, live_server: LiveServer, user: CustomUser, logged_in_page: Page) -> None:
        # Create a tweet
        tweet_content = "This is an E2E test tweet!"
        logged_in_page.fill("textarea[name='content']", tweet_content)
        logged_in_page.click("button[type='submit']")

        # Tweet should appear on the page
        expect(logged_in_page.get_by_text(tweet_content)).to_be_visible()
        # Verify tweet was created in database
        tweet = Tweet.objects.get(content=tweet_content, user=user)
        assert tweet is not None

    def test_like_tweet(self, live_server: LiveServer, user: CustomUser, logged_in_page: Page) -> None:
        # Create a tweet
        tweet_content = "Tweet to be liked!"
        logged_in_page.fill("textarea[name='content']", tweet_content)
        logged_in_page.click("button[type='submit']")

        # Get the tweet ID from the database
        tweet = Tweet.objects.get(content=tweet_content, user=user)

        # Like the tweet using the correct data-testid with tweet ID
        logged_in_page.get_by_test_id(f"like-button-{tweet.id}").click()

        # Verify like was registered (UI should update via HTMX)
        expect(logged_in_page.get_by_test_id(f"like-count-{tweet.id}")).to_contain_text("1")

    def test_retweet(self, live_server: LiveServer, user: CustomUser, logged_in_page: Page) -> None:
        # Create a tweet
        tweet_content = "Tweet to be retweeted!"
        logged_in_page.fill("textarea[name='content']", tweet_content)
        logged_in_page.click("button[type='submit']")

        # Get the tweet ID from the database
        tweet = Tweet.objects.get(content=tweet_content, user=user)

        # Retweet the tweet using the correct data-testid with tweet ID
        logged_in_page.get_by_test_id(f"retweet-button-{tweet.id}").click()

        # Verify retweet was registered
        expect(logged_in_page.get_by_test_id(f"retweet-count-{tweet.id}")).to_contain_text("1")

    def test_follow_user(self, live_server: LiveServer, user: CustomUser, logged_in_page: Page) -> None:
        other_user = CustomUserFactory()

        # Visit the other user's profile
        logged_in_page.goto(f"{live_server.url}/profile/{other_user.username}")

        # Click the follow button
        logged_in_page.get_by_test_id(f"follow-button-{other_user.username}").click()

        # Verify follow was registered (UI should update via HTMX)
        expect(logged_in_page.get_by_test_id(f"follow-button-{other_user.username}")).to_have_text("Unfollow")

        # Verify follower count updated
        expect(logged_in_page.get_by_test_id(f"follower-count-{other_user.username}")).to_contain_text("1")

        # Unfollow the user
        logged_in_page.get_by_test_id(f"follow-button-{other_user.username}").click()

        # Verify unfollow was registered
        expect(logged_in_page.get_by_test_id(f"follow-button-{other_user.username}")).to_have_text("Follow")
        expect(logged_in_page.get_by_test_id(f"follower-count-{other_user.username}")).to_contain_text("0")
