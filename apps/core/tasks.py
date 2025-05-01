from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task
def send_retweet_notification(tweet_id: int, retweeter_username: str) -> None:
    """
    Send an email notification to a user when their tweet is retweeted.
    """
    from apps.core.models import Tweet  # Import here to avoid circular imports

    tweet = Tweet.objects.select_related("user").get(id=tweet_id)
    tweet_author = tweet.user

    subject = f"{retweeter_username} retweeted your tweet!"
    html_message = render_to_string(
        "core/emails/retweet_notification.html",
        {
            "tweet": tweet,
            "retweeter_username": retweeter_username,
        },
    )

    send_mail(
        subject=subject,
        message="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[tweet_author.email],
        html_message=html_message,
    )
