from django.db import models

# Create your models here.


class Contests(models.Model):
    code = models.CharField(max_length=264,blank=True)
    starting = models.DateTimeField(null=True,blank=True)
    duration = models.CharField(max_length=264,null=True,blank=True)
    name = models.CharField(max_length=264,blank=True)
    link = models.CharField(max_length=264,blank=True)
    platform= models.CharField(max_length=264,blank=True)
    ending = models.DateTimeField(null=True,blank=True)
