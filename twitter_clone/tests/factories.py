import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

from ..models import Like, Tweet

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "testpass123")


class TweetFactory(DjangoModelFactory):
    class Meta:
        model = Tweet

    user = factory.SubFactory(UserFactory)
    content = factory.Faker("text", max_nb_chars=280)
    created_at = factory.Faker("date_time")


class LikeFactory(DjangoModelFactory):
    class Meta:
        model = Like

    user = factory.SubFactory(UserFactory)
    tweet = factory.SubFactory(TweetFactory)
