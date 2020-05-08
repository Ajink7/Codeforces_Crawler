from django.db import models

# Create your models here.
class CF_Contest(models.Model):
    contestId = models.IntegerField()
    name = models.CharField(max_length=300)
    writers = models.CharField(max_length=300)
    starting = models.DateTimeField(null=True)
    length = models.CharField(max_length=20)

class CC_Contest(models.Model):
    contestCode = models.CharField(max_length=100)
    name = models.CharField(max_length=300)
    contest_link = models.CharField(max_length=400)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)

class Contests(models.Model):
    code = models.CharField(max_length=264,blank=True)
    starting = models.DateTimeField(null=True,blank=True)
    duration = models.CharField(max_length=264,null=True,blank=True)
    name = models.CharField(max_length=264,blank=True)
    link = models.CharField(max_length=264,blank=True)
