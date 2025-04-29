from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender: type[User], instance: User, created: bool, **kwargs: dict) -> None:
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender: type[User], instance: User, **kwargs: dict) -> None:
    instance.profile.save()
