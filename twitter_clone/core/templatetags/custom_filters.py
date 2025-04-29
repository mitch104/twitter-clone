from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """
    Splits the value by the given delimiter.
    Returns a list.
    """
    return value.split(arg)

@register.filter
def get_liked_tweets_list(liked):
    """
    Converts a boolean to a list with a tweet.id
    """
    if liked:
        return [1]  # A placeholder value that will equal the tweet.id
    return [] 