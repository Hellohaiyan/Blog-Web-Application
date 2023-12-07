from django import forms
from django.forms import TextInput, PasswordInput, EmailInput, FileInput, Textarea
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserAvatar, UserBio

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        labels = {'username': '', 'first_name': '', 'last_name': '', 'email': '', 'password1': '', 'password2': ''}
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': EmailInput(attrs={'class': 'form-control', 'required': True}),
            'password1': PasswordInput(attrs={'class': 'form-control'}),
            'password2': PasswordInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'


class SigninForm(AuthenticationForm):
    class Meta:
        model = User
        labels = {'username': '', 'password': ''}
        fields = ['password', 'password']

    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'


class UserAvatarForm(forms.ModelForm):
    class Meta:
        model = UserAvatar
        fields = ['avatar']
        labels = {'avatar': ''}
        widgets = {
            'avatar': FileInput(attrs={'class': 'form-control', 'type': 'file', 'name': 'avatar', 'aria-label':'Upload'}),
        }

class UserBioForm(forms.ModelForm):
    class Meta:
        model = UserBio
        fields = ['bio']
        labels = {'bio': ''}
        widgets = {
            'bio': Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }

class ChangePasswordForm(UserCreationForm):
    class Meta:
        model = User
        labels = {'password1': '', 'password2': ''}
        fields = ['password1', 'password2']
        widgets = {
        }

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'