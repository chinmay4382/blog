from django import forms
from . models import Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class PostCreateForm(forms.ModelForm):

    class Meta:
        model=Post
        fields = {
            'title',
            'body',
            'status'
        }


class UserLoginForm(forms.Form):
    username=forms.CharField(label='username',widget=forms.TextInput(attrs={'placeholder':'UserName '}))
    password=forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder':'Password '}))


class UserRegistrationForm(UserCreationForm):


    class Meta:
        model = User

        fields = [
            'email',
            'username',
            'password1',
            'password2',
            'is_staff'

        ]
