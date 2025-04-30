from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def split(value: str, arg: str) -> list[str]:
    """
    Splits the value by the given delimiter.
    Returns a list.
    """
    return value.split(arg)


@register.filter
def get_liked_tweets_list(liked: bool) -> list[int]:
    """
    Converts a boolean to a list with a tweet.id
    """
    if liked:
        return [1]  # A placeholder value that will equal the tweet.id
    return []


@register.filter
@stringfilter
def format_username(value: str) -> str:
    """Format username with @ symbol."""
    return f"@{value}"


@register.filter
def format_tweet_content(value: str) -> str:
    """Format tweet content with line breaks."""
    return str(mark_safe(value.replace("\n", "<br>")))
