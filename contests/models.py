from django.db import models

# Create your models here.
class Contest(models.Model):
    contestId = models.IntegerField()
    name = models.CharField(max_length=300)
    writers = models.CharField(max_length=300)
    starting = models.DateTimeField(null=True)
    length = models.CharField(max_length=20)
