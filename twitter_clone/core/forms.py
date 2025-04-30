from typing import Any

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Tweet


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self) -> dict[str, Any]:
        cleaned_data: dict[str, Any] = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']


class TweetForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': "What's happening?"}),
        max_length=280
    )
    image = forms.ImageField(required=False)

    class Meta:
        model = Tweet
        fields = ['content', 'image']


class UserProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Profile
        fields = ['bio']

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'] = forms.CharField(initial=self.instance.user.username)
            self.fields['email'] = forms.EmailField(initial=self.instance.user.email)

    def save(self, commit: bool = True) -> Profile:
        profile: Profile = super().save(commit=False)
        if commit:
            profile.save()
            if 'username' in self.cleaned_data:
                profile.user.username = self.cleaned_data['username']
            if 'email' in self.cleaned_data:
                profile.user.email = self.cleaned_data['email']
            profile.user.save()
        return profile
