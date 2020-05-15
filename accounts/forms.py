from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django import forms
from .models import UserProfile

class UserCreateForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields= ['username','email','password1','password2']

class UserProfileCreateForm(ModelForm):

    class Meta:
        model = UserProfile
        exclude = ['user']
