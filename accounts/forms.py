from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from collections import OrderedDict
class UserCreateForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields= ['username','email','password1','password2']

class UserProfileCreateForm(ModelForm):
    username = forms.CharField(max_length=200,required = True)
    firstname = forms.CharField(max_length=200,required = True)
    lastname = forms.CharField(max_length=200,required = True)
    def __init__(self, *args, **kw):
        super(UserProfileCreateForm, self).__init__(*args, **kw)
        self.fields['firstname'].initial = self.instance.user.first_name
        self.fields['lastname'].initial = self.instance.user.last_name
        self.fields['username'].initial = self.instance.user.username
        Order = (
            'username',
            'firstname',
            'lastname',
            'location',
            'profile_picture',
            'work',
            'education',
            'skills',
            'codeforces_handle',
            'codechef_handle',
            'atcoder_handle',
            'leetcode_handle',
            )
        fields = OrderedDict()
        for key in Order:
            fields[key] = self.fields.pop(key)
        self.fields = fields
    class Meta:
        model = UserProfile
        exclude = ['user']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            if self.fields['username'].initial != username:
                raise forms.ValidationError('Username already exists.')
        return username

    def save(self):
        profile = super().save(commit = False)
        profile.user.username = self.cleaned_data['username']
        profile.user.first_name = self.cleaned_data['firstname']
        profile.user.last_name = self.cleaned_data['lastname']
        profile.save()
        return profile
