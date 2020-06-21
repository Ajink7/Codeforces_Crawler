from django.db import models

# Create your models here.
class submissions(models.Model):
    id1 = models.CharField(max_length = 264 ,blank=True)
    Date = models.DateTimeField(null=True,blank=True)
    user1 = models.CharField(max_length=264,null=True,blank=True)
    Result = models.IntegerField(blank=True)
    Time = models.DecimalField(max_digits=6, decimal_places=5, blank =True )
    mem = models.CharField(max_length=264,null=True,blank=True)
    lang = models.CharField(max_length=264,null=True,blank=True)
    sol = models.CharField(max_length=264,null=True,blank=True)
