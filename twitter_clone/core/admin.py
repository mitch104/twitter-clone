from django.contrib import admin

from .models import Follow, Like, Profile, Tweet


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_joined')
    search_fields = ('user__username', 'user__email')

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'content')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'tweet', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'tweet__content')

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('follower__username', 'following__username')
