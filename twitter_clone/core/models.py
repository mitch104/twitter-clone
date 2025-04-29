from typing import TYPE_CHECKING

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

if TYPE_CHECKING:
    from django.db.models import QuerySet


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"

    def get_following_count(self) -> int:
        return Follow.objects.filter(follower=self.user).count()

    def get_followers_count(self) -> int:
        return Follow.objects.filter(following=self.user).count()

    def get_tweets_count(self) -> int:
        return Tweet.objects.filter(user=self.user).count()


class Tweet(models.Model):
    """Model for tweets."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets")
    content = models.TextField(max_length=280)
    image = models.ImageField(upload_to="tweet_images", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="retweets"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user.username}: {self.content[:50]}"

    def get_likes_count(self) -> int:
        return Like.objects.filter(tweet=self).count()

    def get_retweets_count(self) -> int:
        return Tweet.objects.filter(parent=self).count()

    def is_retweet(self) -> bool:
        return self.parent is not None

    def is_liked_by(self, user: User) -> bool:
        if not user.is_authenticated:
            return False
        return Like.objects.filter(tweet=self, user=user).exists()

    def get_likes(self) -> "QuerySet[User]":
        return User.objects.filter(likes__tweet=self)

    def get_retweets(self) -> "QuerySet[User]":
        return User.objects.filter(retweets__tweet=self)

    def get_replies(self) -> "QuerySet[Tweet]":
        return Tweet.objects.filter(parent=self)


class Like(models.Model):
    """Model for tweet likes."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "tweet")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user.username} likes {self.tweet.content[:50]}"


class Follow(models.Model):
    """Model for user follows."""

    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("follower", "following")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.follower.username} follows {self.following.username}"
