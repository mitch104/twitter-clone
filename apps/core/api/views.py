from django.db.models import Q
from rest_framework import viewsets

from ..models import Tweet
from .permissions import HasAPIKeyOrIsAuthenticated
from .serializers import TweetSerializer


class TweetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows tweets to be viewed.
    """

    serializer_class = TweetSerializer
    permission_classes = [HasAPIKeyOrIsAuthenticated]

    def get_queryset(self):
        """
        Returns tweets from users that the current user follows,
        plus their own tweets.
        """
        following = self.request.user.following.values_list("following", flat=True)
        return (
            Tweet.objects.filter(Q(user__in=following) | Q(user=self.request.user))
            .select_related("user")
            .prefetch_related("likes")
        )
