import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from apps.core.models import CustomUser, Follow, Like, Tweet


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "testpass123")
    bio = factory.Faker("text", max_nb_chars=500)
    date_joined = factory.LazyFunction(timezone.now)


class TweetFactory(DjangoModelFactory):
    class Meta:
        model = Tweet

    user = factory.SubFactory(CustomUserFactory)
    content = factory.Faker("text", max_nb_chars=280)
    created_at = factory.LazyFunction(timezone.now)
    parent = None


class LikeFactory(DjangoModelFactory):
    class Meta:
        model = Like

    user = factory.SubFactory(CustomUserFactory)
    tweet = factory.SubFactory(TweetFactory)
    created_at = factory.LazyFunction(timezone.now)


class FollowFactory(DjangoModelFactory):
    class Meta:
        model = Follow

    follower = factory.SubFactory(CustomUserFactory)
    following = factory.SubFactory(CustomUserFactory)
    created_at = factory.LazyFunction(timezone.now)
