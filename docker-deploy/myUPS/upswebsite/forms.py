from django import forms
from . import models


class UserForm(forms.Form):
    username = forms.CharField(label="username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username",'autofocus': ''}))
    password = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "Password"}))


class RegisterForm(forms.Form):
    username = forms.CharField(label="username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="repeat password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="email", widget=forms.EmailInput(attrs={'class': 'form-control'}))

class TrackForm(forms.Form):
    tracknum = forms.DecimalField(label="tracknum", min_value=0, max_digits=32, decimal_places=0, widget=forms.TextInput(attrs={'class': 'form-control'}))

class DestForm(forms.Form):
    x = forms.DecimalField(label="x", max_digits=32, decimal_places=0, widget=forms.TextInput(attrs={'class': 'form-control'})) 
    y = forms.DecimalField(label="y", max_digits=32, decimal_places=0, widget=forms.TextInput(attrs={'class': 'form-control'}))