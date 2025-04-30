from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Follow, Like, Tweet


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined')
    search_fields = ('username', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('bio',)}),
    )


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
