from typing import Any

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, Tweet


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'password1', 'password2']

    def clean(self) -> dict[str, Any]:
        cleaned_data: dict[str, Any] = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio']


class TweetForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': "What's happening?"}),
        max_length=280
    )
    image = forms.ImageField(required=False)

    class Meta:
        model = Tweet
        fields = ['content', 'image']
