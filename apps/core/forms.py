from typing import Any, cast

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, Tweet


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "bio", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "bio"]


class TweetForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "What's happening?"}),
        max_length=280,
    )
    image = forms.ImageField(required=False)

    class Meta:
        model = Tweet
        fields = ["content", "image"]

    def __init__(self, *args: Any, user: CustomUser | None = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit: bool = True) -> Tweet:
        tweet = cast(Tweet, super().save(commit=False))
        tweet.user = self.user
        if commit:
            tweet.save()
        return tweet
