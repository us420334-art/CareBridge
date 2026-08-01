from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegistrationForm(forms.ModelForm):

    username = forms.CharField(max_length=100)

    email = forms.EmailField()

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile

        fields = [
            'role',
            'phone',
            'address',
        ]