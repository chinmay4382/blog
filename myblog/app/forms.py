from django import forms
from . models import Post
from django.contrib.auth.models import User


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


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password '}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))

    class Meta:
        model = User

        fields = {
            'username',
            'first_name',
            'last_name',
            'email',
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm_password=self.cleaned_data.get('confirm password')
        if password != confirm_password:
            raise(forms.ValidationError(message="Password Mismatch"))
        return confirm_password

