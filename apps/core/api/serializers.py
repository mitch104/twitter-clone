from rest_framework import serializers

from ..models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    likes_count = serializers.IntegerField(source="get_likes_count", read_only=True)
    retweets_count = serializers.IntegerField(source="get_retweets_count", read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_retweet = serializers.BooleanField(read_only=True)

    class Meta:
        model = Tweet
        fields = [
            "id",
            "username",
            "content",
            "image",
            "created_at",
            "likes_count",
            "retweets_count",
            "is_liked",
            "is_retweet",
            "parent",
        ]
        read_only_fields = ["user", "created_at"]

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.is_liked_by(request.user)
        return False
