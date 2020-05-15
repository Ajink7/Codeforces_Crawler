from django.db import models
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.db.models.signals import post_save
# Create your models here.
from django.contrib.auth.models import User
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name ='profile',on_delete=models.CASCADE)
    location = models.CharField(max_length=256,blank = True,null = True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True,null = True)
    work = models.CharField(max_length = 512,blank = True,null = True)
    education =  models.CharField(max_length = 512,blank = True,null = True)
    skills = models.CharField(max_length = 512,blank = True,null = True)
    codeforces_handle = models.CharField(max_length = 256,blank = True,null = True)
    codechef_handle = models.CharField(max_length = 256,blank = True,null = True)
    leetcode_handle = models.CharField(max_length = 256,blank = True,null = True)
    atcoder_handle = models.CharField(max_length = 256,blank = True,null = True)

# def create_profile(sender, instance, created, *args, **kwargs):
#     # ignore if this is an existing User
#     if not created:
#         return
#     UserProfile.objects.create(user=instance)
#
# post_save.connect(create_profile, sender=User)
